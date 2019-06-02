# Library to vectorize text using Doc2Vec model
# Inspired by https://cs.stanford.edu/~quocle/paragraph_vector.pdf,
# https://india.endurance.com/machine-learning-website-categorization/,
# https://towardsdatascience.com/word2vec-from-scratch-with-numpy-8786ddd49e72

import re


def tokenize(text):
    """ Convert string to lowercased tokens with at least 1 letter """
    tokenMatch = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
    return tokenMatch.findall(text.lower())
