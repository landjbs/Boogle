"""
Document vectorization is a method of mapping a text document into a vector
of n values. While the length of this vector is determined by the programmer,
the relative values of different documents are assigned by a machine learning
algorithm trained for word prediction on masked sentences and next sentence
prediciton.
Uses BERT model for document embedding
"""

from bert_serving.client import BertClient # to assign document vectors

import nltk
import smart_open # for opening documents
import multiprocessing # for faster model training
import matplotlib.pyplot as plt
from os import listdir

bc = BertClient(check_length=False)


def vectorize_all(document):
    """
    Vectorizes entire document in single 1024 dim vector using BertClient
    """
    # return document vector for tokenized input doc
    return bc.encode([document])[0]


def vectorize_n_split(document, n):
    """
    Vectorizes document as matrix of vector embeddings of n fractions of the
    document.
    """
    # find size of chunk necessary to fully encode doument in n parts
    chunkSize = len(document) / n
    ### TO COMPLETE ###
    return None


def docVec_to_dict(docVec):
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
