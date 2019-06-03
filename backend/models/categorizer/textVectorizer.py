# Library to vectorize text using Doc2Vec model
# Inspired by https://cs.stanford.edu/~quocle/paragraph_vector.pdf,
# https://india.endurance.com/machine-learning-website-categorization/,
# https://towardsdatascience.com/word2vec-from-scratch-with-numpy-8786ddd49e72

import re
import numpy as np
import pandas as pd
from os import listdir # for navigating training data
import pickle

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
    pageVector = {word:(word_to_scalar(word, freqDict[word])) for word in freqDict}

    return pageVector


## test vector method for sentiment analysis ##
# 0 = positive
# 1 = negative
def gen_data():
    dataList = []

    path = 'aclImdb/train/pos'

    for count, file in enumerate(os.listdir(path)):
        FileObj =  open(f"{path}/{file}", 'r')
        pageText = "".join([line for line in FileObj])
        pageVector = vectorize_pageText(pageText)
        pageVector.update({'sentiment':0})
        dataList.append(pageVector)
        print(f"\tAnalyzing {path}: {count}", end="\r")
        if count > 1000:
            print("\n")
            break

    path = 'aclImdb/train/neg'

    for count, file in enumerate(os.listdir(path)):
        FileObj =  open(f"{path}/{file}", 'r')
        pageText = "".join([line for line in FileObj])
        pageVector = vectorize_pageText(pageText)
        pageVector.update({'sentiment':1})
        dataList.append(pageVector)
        print(f"\tAnalyzing {path}: {count}", end="\r")
        if count > 1000:
            print("\n")
            break

    testDF = pd.DataFrame(dataList)

    print(testDF.head(), end=f"\n{'-'*60}\n")

    def save(object, path):
        """ Saves object to path. Wraps pickle for consolidated codebase. """
        file = open(path, "wb")
        pickle.dump(object, file)
        print(f"Object successfully saved to {path}.")

    save(testDF, 'testDF.obj')

gen_data()

# MODEL STUFF #
# open testDF from saved object
def load(path):
    """ Loads object from path. Wraps pickle for consolidated codebase. """
    file = open(path, "rb")
    object = pickle.load(file)
    return object

testDF = load('testDF.obj')

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical

model = Sequential([
    Dense(300, input_shape=(4352,)),
    Activation('relu'),
    Dense(2),
    Activation('softmax'),
])

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

trainDF = testDF.copy()
trainDF.drop("sentiment",axis=1)

model.fit(trainDF, to_categorical(testDF['sentiment']), epochs=10)



pass
