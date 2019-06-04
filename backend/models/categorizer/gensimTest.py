from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.parsing.preprocessing import remove_stopwords, strip_numeric
import nltk
from os import listdir # for
import smart_open # for opening documents
# ignore warnings
import warnings
warnings.simplefilter("ignore")
import re


def clean_tokenize(inStr):
    """ Converts string to clean, lowercase list of tokens """
    # lowercase inStr, filter out common stop words and numerics
    cleanStr = strip_numeric(remove_stopwords(inStr.lower()))
    # tokenize cleanStr by whitespace
    tokens = nltk.tokenize.word_tokenize(cleaStr))
    return cleanTokens


def train_d2v(data, path='d2v.model', max_epochs=100, vec_size=300, alpha=0.025):
    """ Trains doc vectorization model on iterable of docs and saves model to path """
    print(f"\n{'-'*40}\nTraining '{path}' model:")

    # list mapping list of document tokens to unique integer tag
    tagged_data = [TaggedDocument(words=clean_tokenize(_d), tags=[str(i)]) for i, _d in enumerate(data)]
    print(f"\tData Tagged (length={len(tagged_data)})")

    # initialize model
    model = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)

    # build vector of all words contained in tagged data
    model.build_vocab(tagged_data)
    print(f"\tVocab Built\n\tModel Training for {max_epochs} epochs")

    # train model for max_epochs
    for epoch in range(max_epochs):
        print(f'\t\tEpoch: {epoch}', end="\r")
        model.train(tagged_data,
                    # signify that tagged_data is what was used to build vocab
                    total_examples=model.corpus_count,
                    # signify that train is only called once for efficiency
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    # save model to path
    model.save(path)
    print(f"Model saved to '{path}'.\n{'-'*40}")


def vectorize_document(doc, modelPath="d2v.model"):
    """ Vectorizes document with d2v model stored at modelPath """
    # load saved model
    model= Doc2Vec.load("d2v.model")
    # tokenize input doc
    tokenizedDoc = nltk.tokenize.word_tokenize(doc.lower())
    # create document vector for tokenizedDoc
    docVector = model.infer_vector(tokenizedDoc)
    return docVector


dataList = []

path = 'aclImdb/train/pos'

print("Positive")
for count, file in enumerate(listdir(path)):
    FileObj =  smart_open.open(f"{path}/{file}", 'r')
    pageText = "".join([line for line in FileObj])
    dataList.append(pageText)
    print(f"\tAnalyzing {path}: {count}", end="\r")
    if count > 10:
        print("\n")
        break

path = 'aclImdb/train/neg'
print("Negative")
for count, file in enumerate(listdir(path)):
    FileObj =  smart_open.open(f"{path}/{file}", 'r')
    pageText = "".join([line for line in FileObj])
    dataList.append(pageText)
    print(f"\tAnalyzing {path}: {count}", end="\r")
    if count > 10:
        print("\n")
        break

train_d2v(dataList, path='test.model')

dataList = ['good', 'great', 'fine', 'amazing', 'awful', 'bad', 'terrible', 'king', 'queen']

docVectors = []

for doc in dataList:
    docVectors.append(vectorize_document(doc, modelPath='test.model'))

from scipy.spatial import distance

import numpy as np

distMatrix = np.zeros((len(dataList), len(dataList)))

for i, curVector in enumerate(docVectors):
    for j, otherVector in enumerate(docVectors):
        dist = distance.euclidean(curVector, otherVector)
        distMatrix[i,j] = dist
    print(f"\t{i}", end='\r')

import matplotlib.pyplot as plt

plt.imshow(distMatrix)
plt.show()





















pass
