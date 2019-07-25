"""
Document vectorization is a method of mapping a text document into a vector
of n values. While the length of this vector is determined by the programmer,
the relative values of different documents are assigned by a machine learning
algorithm trained for word prediction on masked sentences and next sentence
prediciton.
Uses BERT model for document embedding
"""

from math import floor
import numpy as np
from termcolor import colored
import appscript
from bert_serving.client import BertClient # to assign document vectors
import matplotlib.pyplot as plt

# bert-serving-start -model_dir /Users/landonsmith/Desktop/uncased_L-24_H-1024_A-16 -num_worker=1


bc = BertClient(check_length=False)


def vectorize_doc(document):
    """
    Vectorizes entire document in single 1024 dim vector using BertClient
    """
    # return document vector for tokenized input doc
    return bc.encode([document])[0]


def vectorize_n_split(document, n):
    """
    Vectorizes document as matrix of vector embeddings of n fractions of the
    document. Chunks are delimited by whitespace by not by sentence endings
    and vary in size by up to n-1. Returned docMatrix will always be (n, 1024)
    """
    # split document into words and find length
    words = document.split()
    numWords = len(words)
    # split words into n roughly-even-sized chunks--method function of (n, numWords)
    if numWords < n:
        raise ValueError(f'Document must have more than {n} words')
    elif ((numWords % n) == 0):
        chunkSize = int(numWords / n)
        chunkMatrix = [" ".join(words[i:i+chunkSize])
                        for i in range(0, numWords, chunkSize)]
    else:
        # calculate size of first chunk and size of others
        baseChunkSize = floor(len(words) / n)
        firstChunkSize = baseChunkSize + (numWords % n)
        # initialize chunkMatrix and add first chunk
        chunkMatrix = []
        chunkMatrix.append(" ".join(words[0:firstChunkSize]))
        # add remaining chunks of baseChunkSize
        for i in range(firstChunkSize, numWords, baseChunkSize):
            chunkMatrix.append(" ".join(words[i:i+baseChunkSize]))
    # create matrix of vectorized chunks
    docMatrix = np.array([vectorize_doc(chunk) for chunk in chunkMatrix])
    return docMatrix


# import re
# def vectorize_sentence_split(document, n):
#     sentences = [sentence.strip() for sentence in re.split(r'[/.|!|?|"|;]', document)]
#     numSentences = len(sentences)
#     if numSentences > n:
#         raise ValueError(f'Sentence number must be greater than {n}.')
#     elif ((numSentences % n) == 0):
#         chunkSize = int(numSentences / n)
#         chunkMatrix = [" ".join(sentences[i:i+chunkSize])
#                         for i in range(0, numSentences, chunkSize)]
#     else:



def vectorize_doc_list(docList):
    """ Returns list of vector representation of each doc in docList """
    vecList = bc.encode(docList)
    return vecList

def score_doc_list(docList):
    """ Returns list of tuples of form (docVector, docContents) """
    return [(vectorize_doc(doc), doc) for doc in docList]

def vec_to_dict(docVec):
    """ Converts docVec to dict for easy df insertion """
    return {dimension:value for dimension, value in enumerate(docVec)}


def visualize_vecDict(vecDict):
    """ Plots dict mapping titles to docVecs to determine differences """
    for url in vecDict:
        plt.plot(vecDict[url])
    plt.legend([key for key in vecDict])
    plt.title(f'Vectors for {len(vecDict)} Documents')
    plt.xlabel('Vector Dimensions')
    plt.ylabel('Document Value')
    plt.show()
