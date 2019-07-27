import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.regularizers import l2

from scipy.stats import kurtosis, skew
from scipy.spatial.distance import euclidean

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


answerDf = pd.read_pickle('data/outData/searchAnalysis/answeringDf2500.sav')
print(answerDf.head())

answerList = []
for row in answerDf.iterrows():
  rowInfo = row[-1]
  distVec = np.subtract(rowInfo['paraVec'], rowInfo['questionVec'])
  rowDict = {dim:scalar for dim,scalar in enumerate(distVec)}
  rowDict.update({'score': rowInfo['score']})
  answerList.append(rowDict)

trainableDf = pd.DataFrame(answerList)
print(trainableDf.head())

# reindex the data
trainableDf = trainableDf.reindex(np.random.permutation(trainableDf.index))

targets = trainableDf['score']
features = trainableDf.drop(columns=['score'])

meanScore = np.mean(targets)
print(f'Mean Score: {meanScore}')

# normalize the features
normedFeatures = pd.DataFrame(StandardScaler().fit_transform(X=features))
print(normedFeatures.describe())

# model training
model = Sequential()

# input layer
model.add(Dense(30, activation='relu', input_dim=(normedFeatures.shape)[1]))
# first hidden layer
model.add(Dense(100, activation='relu'))
# second hidden layer
model.add(Dense(100, activation='relu', kernel_regularizer=l2(0.01)))
# output layer
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer ='adam',loss='binary_crossentropy', metrics =['accuracy'])

model.fit(np.array(normedFeatures), targets, validation_split=0.1, epochs=15)

model.save('data/outData/searchAnalysis/paragraphAnswering.sav')
