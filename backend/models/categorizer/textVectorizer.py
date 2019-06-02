# Library to vectorize text using Doc2Vec model
# Inspired by https://cs.stanford.edu/~quocle/paragraph_vector.pdf,
# https://india.endurance.com/machine-learning-website-categorization/,
# https://towardsdatascience.com/word2vec-from-scratch-with-numpy-8786ddd49e72

import re
import numpy as np

# matcher for tokenizing words
tokenString = r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*'
tokenMatcher = re.compile(tokenString)

def tokenize(text):
    """ Convert string to lowercased tokens with at least 1 letter """
    tokenList = tokenMatcher.finall(text.lower())
    return tokenList

def build_wordVector(tokenList):
    """ Creates n-length vector for binary representation of words where n=numWords """
    wordSet = set()
    for token in tokenList:
        wordSet.add(token)
    wordVector = list(wordSet)
    return wordVector
