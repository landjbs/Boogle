# Library to vectorize text using Doc2Vec model
# Inspired by https://cs.stanford.edu/~quocle/paragraph_vector.pdf,
# https://india.endurance.com/machine-learning-website-categorization/,
# https://towardsdatascience.com/word2vec-from-scratch-with-numpy-8786ddd49e72

import re
import numpy as np
import pandas as pd

# matcher for tokenizing words
tokenString = r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*'
tokenMatcher = re.compile(tokenString)

def tokenize(text):
    """ Convert string to lowercased tokens with at least 1 letter """
    tokenList = tokenMatcher.findall(text.lower())
    return tokenList

def build_wordVector(tokenList):
    """ Creates n-length vector for binary representation of words where n=numWords """
    wordSet = set()
    for token in tokenList:
        wordSet.add(token)
    wordVector = list(wordSet)
    return wordVector

# read int frequency df and convert datatypes
frequencyDF = pd.read_csv("frequencyData.csv", sep=",",
                            names=['Rank', 'Word', 'Part of speech',
                                    'Frequency', 'Dispersion'],
                            usecols=[1,2,3,4],
                            dtype={'Range':np.int32, 'Frequency':np.int32,
                                    'Dispersion':np.float32},
                            skiprows=[0,1])


for i in list(frequencyDF['Word']):
    assert isinstance(i, str), "noppe"
