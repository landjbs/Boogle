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


### FREQUENCY-BASED BOW MODEL ###
# read int frequency df and convert datatypes
frequencyDF = pd.read_csv("frequencyData.csv", sep=",",
                            names=['Rank', 'Word', 'Part of speech',
                                    'Frequency', 'Dispersion'],
                            usecols=[1,2,3,4],
                            dtype={'Range':np.int32, 'Frequency':np.int32,
                                    'Dispersion':np.float32},
                            skiprows=[0,1])

# convert frequency to relative frequency
useSum = np.sum(frequencyDF['Frequency'])
frequencyDF['Frequency'] = frequencyDF['Frequency'].apply(lambda curFreq : curFreq/useSum)

# remove \xa0\xa0\xa0 (non-break space) from word starts
frequencyDF['Word'] = frequencyDF['Word'].apply(lambda word : word.replace(u'\xa0', u''))

# create freqDict: maps words to expected frequency
freqDict = dict(zip(frequencyDF['Word'], frequencyDF['Frequency']))

def vectorize_pageText(pageText):
    """ Converts words in pageText into vector of probabilities """
    # convert pageText to list of tokens
    pageTokens = tokenize(pageText)
    # store number of tokens for normalization
    numTokens = len(pageTokens)
    # convert tokens back into string for vectorization
    tokenText = " ".join(pageTokens)

    def word_to_scalar(word, frequency):
        """ Helper to scan page text for word occurences and normalize by frequency """
        normalizedFreq = len(re.findall(word, tokenText)) / (numTokens * frequency)
        return normalizedFreq

    # create vector of normalized scalars for each word in freqDict
    pageVector = [vectorize_word(word, freqDict[word]) for word in freqDict]

    return pageVector








pass
