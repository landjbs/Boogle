import re
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
from scipy.spatial.distance import euclidean

import models.binning.docVecs as docVecs
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from models.knowledge.knowledgeFinder import find_rawTokens

binopList = ['+', '-', '?', '==']
unopList = ['(', ')']
unopMatcher = re.compile(r'[(|)]')

def bert_parser(inStr):
    tokens = inStr.split()
    tokenNum = len(tokens)
    if (tokenNum==0):
        raise ValueError("Cannot parse empty string.")
    elif (tokenNum==1):
        cleanToken = re.sub(unopMatcher, '', tokens[0])
        return docVecs.vectorize_doc(cleanToken)
    else:
        evaluateTokens = re.findall(r'(?<=\()[^)]+(?=\))', inStr)
        vectorizedTokens = {token:docVecs.vectorize_doc(token) for token in evaluateTokens}
        for i, token in enumerate(tokens):
            cleanToken = re.sub(unopMatcher, '', token)
            if cleanToken in vectorizedTokens:
                tokens[i] = vectorizedTokens[cleanToken]
        for i in range(0, len(tokens), 3):
            token1 = tokens[i]
            token2 = tokens[i+2]
            operator = tokens[i+1]
            print(token1, token2, operator)
            print(bert_binop(token1, token2, operator))

def find_subs(inStr):
    numOpen = 0
    subsList = []
    readText = ""
    for c in inStr:
        if c == '(':
            numOpen += 1
        elif c == ')':
            numOpen -= 1
            if numOpen == 0:
                subsList.append(readText)
                readText = ""
        if numOpen == 0:
            pass
        else:
            readText += c
    return subsList


def bert_multiParser(inStr):
    # words = re.findall(r'(?<=\()[^)]+(?=\))', inStr)
    # expressions = re.findall(r'(?<=\().+(?=\))', inStr)
    # for expression in expressions:
    #     # words = expression.split()
    expression = re.findall(r'(?<=\().+(?=\))', inStr)
    subExpressions = find_subs(expression[0])
    if len(subExpressions)==1:
        return docVecs.vectorize_doc(subExpressions[0])
    elif len(subExpressions)==2:
        left = bert_multiParser(subExpressions[0])
        right = bert_multiParser(subExpressions[1])
        leftEnd = (expression[0].find(subExpressions[0])) + len(subExpressions[0])
        rightStart = expression[0].find(subExpressions[1])
        operator = re.findall(r'[?|==|\-|\+]', expression[0][leftEnd:rightStart])
        return bert_binop(left, right, operator[0])

    # if len(subExpressions)==1:
    #     print(subExpressions)
    #     return docVecs.vectorize_doc(subExpressions[0])
    # elif len(subExpressions)==3:
    #     operator = subExpressions[1]
    #     parsedFirst = bert_multiParser(subExpressions[0])
    #     parsedLast = bert_multiParser(subExpressions[2])
    #     return bert_binop(parsedFirst, parsedLast, operator)


# def bert_unop(vec1, operator):
#     """ Performs unary operation from unopList on vec1 """
#


def bert_binop(vec1, vec2, operator):
    """ Performs binary operation from binopList on vec1 on vec2 """
    assert (len(vec1)==len(vec2)==1024), "Vectors must both have length of 1024"
    if (operator=='+'):
        return np.add(vec1, vec2)
    elif (operator=='-'):
        return np.subtract(vec1, vec2)
    elif (operator=='?'):
        return euclidean(vec1, vec2)
    elif (operator=='=='):
        return (vec1 == vec2)
    else:
        raise ValueError(f"Invalid operator '{operator}'")

def bert_arthimetic(inStr):
    """ inStr must have form 'TERM_1 [+|-] TERM_2 '"""
    splitStrs = inStr.split()
    numTokens = len(splitStrs)

    if (numTokens==1):
        return docVecs.vectorize_doc(splitStrs)

    elif (numTokens==3):
        operator = splitStrs[1]
        vecs = docVecs.vectorize_doc_list([splitStrs[0], splitStrs[2]])
        # identify arthimetic method
        if (operator=='+'):
            return np.add(vecs[0], vecs[1])
        elif (operator=='-'):
            return np.subtract(vecs[0], vecs[1])
        else:
            raise ValueError('Invalid operator')


def vectorize_masked_tokens(document, maskToken='', knowledgeProcessor=None, scoringMethod='euclidean', disp=False):
    """
    Iteratively masks all knowledge tokens in document string and determines
    score relative to initial vector. Returns dict of token and score
        -document: string of the document to vectorize
        -maskToken: string to replace each token with
        -knowledgeProcessor: knowledge tokens to locate, will be built from document if not given
        -scoringMethod: use euclidean distance or dot product to determine distance from baseVec
        -disp: whether to display the bar chat of distances
    """
    # assertions and special conditions
    assert isinstance(document, str), "document must have type 'str'"
    assert isinstance(maskToken, str), "maskToken must have type 'str'"
    assert (scoringMethod in ['euclidean', 'dot']), "scoringMethod must be 'euclidean' or 'dot'"

    if not knowledgeProcessor:
        knowledgeProcessor = build_knowledgeProcessor(document.split())

    # define scoring method
    if (scoringMethod=='euclidean'):
        def calc_score(maskedVec, baseVec):
            return euclidean(maskedVec, baseVec)
    elif (scoringMethod=='dot'):
        def calc_score(maskedVec, baseVec):
            return np.sum(maskedVec * baseVec) / np.linalg.norm(baseVec)

    # calculate vector of raw document
    baseVec = docVecs.vectorize_doc(document)

    # find tokens in document with both greedy and non-greedy matching
    foundTokens = find_rawTokens(document, knowledgeProcessor)

    scoreDict = {}

    for token in foundTokens:
        print(colored(f'\t{token}', 'red'), end=' | ')
        maskedDoc = re.sub(token, maskToken, document)
        maskedVec = docVecs.vectorize_doc(maskedDoc)
        score = calc_score(maskedVec, baseVec)
        print(colored(score, 'green'))
        scoreDict.update({token:score})

    if disp:
        plt.bar(scoreDict.keys(), scoreDict.values())
        plt.ylabel('Euclidean Distance from Base Vector')
        plt.title(f'Tokens Iteratively Replaced With "{maskToken}"')
        plt.show()

    return scoreDict


def word_vs_sentence(document):
    tokens = document.split()

    docVec = docVecs.vectorize_doc(document)

    vecList = [docVecs.vectorize_doc(token) for token in tokens]

    maxList = []

    for i, vec in enumerate(vecList):
        cumDist = np.sum([euclidean(vec, other) for other in vecList])
        print(tokens[i], cumDist)
        maxList.append((cumDist, tokens[i]))

    print(f"\n{max(maxList)}\n")
