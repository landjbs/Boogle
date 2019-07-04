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
from misc.decorators import log_completion


# appscript.app('Terminal').do_script('bert-serving-start -model_dir /Users/landonsmith/Desktop/uncased_L-24_H-1024_A-16 -num_worker=1')

@log_completion(taskString='Connecting to BERT Client')
def import_bert(*args, **kwargs):
    return BertClient(*args, **kwargs)

bc = import_bert(check_length=False)

def vectorize_all(document):
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
    # split words into n roughly-even-sized chunks
    if numWords < n:
        raise ValueError(f'Document must have more than {n} words')
    elif ((numWords % n) == 0):
        chunkSize = int(numWords / n)
        chunkMatrix = [" ".join(words[i:i+chunkSize])
                        for i in range(0, len(words), chunkSize)]
    else:
        # calculate size of first chunk and size of others
        baseChunkSize = floor(len(words) / n)
        firstChunkSize = baseChunkSize + (numWords % n)
        # initialize chunkMatrix and add first chunk
        chunkMatrix = []
        chunkMatrix.append(" ".join(words[0:firstChunkSize]))
        # add remaining chunks of baseChunkSize
        for i in range(firstChunkSize, len(words), baseChunkSize):
            chunkMatrix.append(" ".join(words[i:i+baseChunkSize]))
    # create matrix of vectorized chunks
    docMatrix = np.array([vectorize_all(chunk) for chunk in chunkMatrix])
    return docMatrix


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
