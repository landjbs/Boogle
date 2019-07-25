import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

import models.binning.docVecs as docVecs


class ClusterDict():
    def __init__(self, wordSet={}, inPath="", outPath=""):
        if (wordSet != {}):
            dataList = []
            for word in wordSet:
                wordVec = docVecs.vectorize_doc(word)
                wordDict = docVecs.vec_to_dict(wordVec)
                wordDict.update({'word':word})
                wordDict.update({'vec':wordVec})
                dataList.append(wordDict)
                print(f'Building Database: {word}', end='\r')
            df = pd.DataFrame(dataList)
            self.data = df
        elif (inPath != ""):
            self.data = pd.read_pickle(inPath)
        else:
            raise ValueError('Valid load data must be given.')
        print(self.data.head())
        if not (outPath==""):
            df.to_pickle(outPath)


    def find_nearest_simple(self, newWord, n=5):
        newVec = docVecs.vectorize_doc(newWord)
        # find distances between each word and new word
        calc_dist = lambda curVec : euclidean(newVec, curVec)
        print(newVec)
        df = self.data
        nearestWords = []
        for row in df.iterrows():
            row = (row[-1])
            dist = euclidean(newVec, row['vec'])
            word = row['word']
            nearestWords.append((dist, word))
        nearestWords.sort()
        return nearestWords[:n]
        

    def find_nearest(self, newWord, n=5):
        # vectorize newWord
        newVec = docVecs.vectorize_doc(newWord)
        # find distances between each word and new word
        calc_dist = lambda curVec : euclidean(newVec, curVec)
        df = self.data
        df['dist'] = df['vec'].apply(calc_dist)
        # build df of n closest words to newWord
        distList = list(df['dist'].copy())
        distList.sort()
        SUB_CLUST_SIZE = 50
        cutoffLoc = (min(len(distList), SUB_CLUST_SIZE) - 1)
        cutoffDist = distList[cutoffLoc]
        inClust = (df['dist']<=(cutoffDist))
        clustDf = df[inClust]
        # find standard deviation of dimensions within clustDf
        clustMetrics = clustDf.describe()
        clustMetrics = clustMetrics.drop(columns=['dist'])
        iDevs = list(map(lambda std:1/std, clustMetrics.loc['std']))
        plt.plot(iDevs)
        plt.show()
        # compute dot product within clustDf and newWord with weightings
        # as 1/std for each dimension
        nearestWords = []
        for row in clustDf.iterrows():
            row = row[-1]
            rowDist = euclidean(row['vec'], newVec, w=iDevs)
            print(row['word'], rowDist)
            nearestWords.append((rowDist, row['word']))
        nearestWords.sort()
        return nearestWords[:n]
