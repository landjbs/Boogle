import sys, os
from gensim.parsing.preprocessing import remove_stopwords, strip_numeric
from nltk.tokenize import word_tokenize
sys.path.append(os.path.abspath(os.path.join('..', 'knowledgeClassifier')))
from knowledgeTokenizer import knowledgeTokenize_search

from gensim.parsing.preprocessing import STOPWORDS

def possible_tokens(tokenList):
    """ Finds all possible tokens in a list up to length of list """
    for token in tokenList:
        print(token)

def clean_tokenize(inStr):
    """ Converts string to clean, lowercase list of tokens """
    # lowercase inStr, filter out common stop words and numerics
    cleanStr = inStr.lower()
    # tokenize cleanStr by whitespace
    tokenList = word_tokenize(cleanStr)
    possible_tokens(tokenList)
    return tokenList

knowledgeSet = load('knowledgeTokens.set')

while True:
    query = clean_tokenize(input("Search: "))
    knowledgeTokenize_search(query, knowledgeSet)
