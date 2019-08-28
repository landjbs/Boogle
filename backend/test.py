# config_file = '/Users/landonsmith/Desktop/shortBert/bert_config.json'
# checkpoint_file = '/Users/landonsmith/Desktop/shortBert/bert_model.ckpt'
import numpy as np
from operator import itemgetter

def make_random(size=100):
    return list(zip(np.random.randint(0,10, size=size),
                list(map(chr, np.random.randint(97, 122, size=size)))))

database = {'dirt':make_random() ,'cowboy':make_random()}

def score_token_intersection(pageTup):
    return pageTup[0]

def initialize_result_list(tokenScores, database, n):
    # get most important token
    importantToken = max(tokenScores, key=(lambda elt:tokenScores[elt]))
    importantBucket = database[importantToken]
    otherTokens = tokenScores.pop(importantToken)
    resultList = importantBucket[:n]
    resultLen = len(resultList)

    


def weighted_and_search(tokenScores, database, n):
    # get most important token
    importantToken = max(tokenScores, key=(lambda elt:tokenScores[elt]))
    importantBucket = database[importantToken]
    # initialize result list
    resultList = importantBucket[:n]
    if len(resultList) < n:

    importantBucket = importantBucket[n:]
    otherTokens = tokenScores.copy()
    _ = otherTokens.pop(importantToken)
    bucketList = [database[token] for token in otherTokens]
    # initialize result list
    firstResult = bucketList[0].pop(0)
    curMin = score_token_intersection(firstResult)
    newTup = (curMin, firstResult[1])
    resultList = [newTup]
    scoreList = [curMin]
    for bucket in bucketList:
        for pageTup in bucket:
            score = score_token_intersection(pageTup)
            if score > curMin:
                newTup = (score, pageTup[1])
                resultList.append(pageTup)
                scoreList.append(score)
                if len(resultList) > n:
                    minIndex = scoreList.index(curMin)
                    resultList.remove(minIndex)
                    scoreList.remove(minIndex)
                    curMin = min(resultList, key=itemgetter(0))[0]

    resultList.sort(reverse=True, key=itemgetter(0))
    return resultList

from time import time
s = time()
fake = (weighted_and_search({'dirt':0, 'cowboy':0}, database, 20))
print(f'Time: {time() - s}')


def real_sort(tokenScores, database, n):
    bucketList = [database[token] for token in tokenScores]
    resultList = []
    for bucket in bucketList:
        resultList += [(score_token_intersection(pageTup), pageTup[1])
                        for pageTup in bucket]
    resultList.sort(reverse=True, key=itemgetter(0))
    return resultList[:n]

s2 = time()
real = real_sort({'dirt':0, 'cowboy':0}, database, 20)
print(f'Time: {time() - s2}')
import matplotlib.pyplot as plt

plt.plot([t[0] for t in fake])
plt.plot([t[0] for t in real])
plt.title('Score Moving Avg')
plt.xlabel('Posting Loc')
plt.ylabel('Score')
plt.show()



def _weighted_and_search(tokenScores, database, n):
    bucketList = [database.search_full(key=token, n=100000)
                    for token in tokenScores]
    # get number of pages avaliable to return
    avaliableResults = 0
    for bucket in bucketList:
        avaliableResults += len(bucket)
    # actual number of results to find
    resultNum = min(n, avaliableResults)
    # list to hold ~sorted Page() objects of results
    resultList = []
    # iterate over number of results to show
    for i in range(resultNum):
        topList = []
        for index, bucket in enumerate(bucketList):
            try:
                pageObject = bucket[0][1]
                pageScore = score_token_intersection(pageObject, tokenScores)
                topList.append((pageScore, index))
            except:
                pass
        if topList == []:
            return (len(resultList), resultList)
        maxLoc = max(topList)[1]
        nextAddition = (bucketList[maxLoc].pop(0))[1]
        resultList.append(nextAddition)
    return (resultNum, resultList)
