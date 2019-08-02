import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import h5py
import pickle

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.regularizers import l2
from sklearn.preprocessing import StandardScaler


def build_question_format_model():
    goodQuestionList = []

    goodQuestionDf = pd.read_pickle('data/outData/searchAnalysis/realQueryDf.sav')
    for vec in goodQuestionDf['vec']:
      rowDict = {dim: scalar for dim,scalar in enumerate(vec)}
      rowDict.update({'score':1})
      goodQuestionList.append(rowDict)

    goodQuestionDf = pd.DataFrame(goodQuestionList)


    badQuestionList = []

    badQuestionDf = pd.read_pickle('data/outData/searchAnalysis/fakeQueryDf.sav')
    for row in badQuestionDf.iterrows():
      rowInfo = row[-1]
      rowVec = rowInfo['vec']
      rowDict = {dim:scalar for dim,scalar in enumerate(rowVec)}
      rowDict.update({'score':0})
      badQuestionList.append(rowDict)

    badQuestionDf = pd.DataFrame(badQuestionList)

    questionAnalysisDf = pd.concat([goodQuestionDf, badQuestionDf], ignore_index=True)

    # reindex the data
    questionAnalysisDf = questionAnalysisDf.reindex(np.random.permutation(questionAnalysisDf.index))

    targets = questionAnalysisDf['score']
    features = questionAnalysisDf.drop(columns=['score'])

    meanScore = np.mean(targets)
    print(f'Mean Score: {meanScore}')

    # normalize the features
    normedFeatures = pd.DataFrame(StandardScaler().fit_transform(X=features))
    normedFeatures.describe()

    # model training
    model = Sequential()

    # input layer
    model.add(Dense(30, activation='relu', input_dim=(normedFeatures.shape)[1]))
    # first hidden layer
    model.add(Dense(100, activation='relu'))
    # second hidden layer
    model.add(Dense(100, activation='relu', kernel_regularizer=l2(0.02)))
    # output layer
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer ='adam',loss='binary_crossentropy', metrics =['accuracy'])

    model.fit(np.array(normedFeatures), targets, validation_split=0.1, epochs=15)


    from dataStructures.objectSaver import save

    model.save('data/outData/searchAnalysis/queryFormatModel.h5')

    print('saved')

    return model
