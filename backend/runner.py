"""
Modified pageRank testing
"""
import numpy as np
from time import time
from operator import itemgetter

# bucket_1 = [(2, 'a'), (1, 'b')]
# bucket_2 = [(3, 'c'), (0, 'd')]
# bucket_3 = [(10, 'l'), (5,'z')]
# bucket_4 = [(1000, 'v')]
#
# bucketList = [bucket_1, bucket_2, bucket_3, bucket_4]


def make_list(c, top=100, listLength=1000000):
    l =  list(zip(np.random.randint(0, top, size=listLength), [c for _ in range(listLength)]))
    l.sort(reverse=True, key=itemgetter(0))
    return l

bucket_1 = make_list('a')
bucket_2 = make_list('b', top=1000)
bucket_3 = make_list('c')
bucket_4 = make_list('d')

bucketList = [bucket_1, bucket_2, bucket_3, bucket_4]


def merge_lists(bucketList, maxResultNum):
    s = time()
    resultNum = min(maxResultNum, np.sum([len(bucket) for bucket in bucketList]))
    resultList = []
    for _ in range(resultNum):
        topList = []
        for index, bucket in enumerate(bucketList):
            try:
                topList.append((bucket[0][0], index))
            except:
                pass

        maxLoc = max(topList)[1]
        nextAddition = bucketList[maxLoc].pop(0)
        resultList.append(nextAddition)

    return resultList

timeList = []
for i in range(100):
    stime = time()
    print(merge_lists(bucketList, maxResultNum=10), end='\r')
    timeList.append((time() - stime))
    print(f'iterating: {i}', end='\r')

print(np.mean(timeList))

# from searchers.modelBuilders.questionAnsweringModel import train_answering_lstm
#
#
# train_answering_lstm(folderPath='data/outData/searchAnalysis/squadDataframes',
#                     outPath='questionAnsweringModel.sav')


# import numpy as np
# import matplotlib.pyplot as plt
# from time import time
# from itertools import chain
# from collections import Counter
# from scipy.special import softmax
#
# from dataStructures.objectSaver import load
#
#
# corrDict = load('data/outData/knowledge/relationshipDict.sav')
#
# while True:
#     tokenSearch = input('token: ')
#     if tokenSearch == '//':
#         break
#     try:
#         relTokens = corrDict[tokenSearch]
#         print(f'\t{tokenSearch}')
#         for score, token in relTokens[:5]:
#             print(f'\t\t<{score}> {token}')
#     except:
#         print('None Found')
#

# class PageTest():
#     def __init__(self, name, knowledgeTokens):
#         self.name = name
#         self.knowledgeTokens = knowledgeTokens
#
#     def add_shadow_tokens(self, cutoff=0.2):
#         knowledgeTokens = self.knowledgeTokens
#         relCounts = Counter()
#         for knowledgeToken, knowledgeScore in knowledgeTokens.items():
#             if knowledgeToken in corrDict:
#                 relatedTokens = corrDict[knowledgeToken]
#                 for relatedScore, relatedToken in relatedTokens:
#                     weightedScore = knowledgeScore * relatedScore
#                     if weightedScore > cutoff:
#                         relCounts.update({relatedToken : weightedScore})
#         # update knowledgeTokens
#         knowledgeCounter = Counter(knowledgeTokens)
#         knowledgeCounter.update(relCounts)
#         self.knowledgeTokens = knowledgeCounter
#
# # target = microwave
# electronicStore = PageTest(name='electronicStore', knowledgeTokens={'television':0.5,
#                                                         'radio':0.5,
#                                                         'refrigerator':0.3,
#                                                         'store':0.5})
# movieReviews = PageTest(name='movieReviews', knowledgeTokens={'movie':0.8,
#                                                             'best':0.7,
#                                                             'kids':0.1,
#                                                             'top':0.8,
#                                                             'critic':0.1})
# videoGames = PageTest(name='videoGames', knowledgeTokens={'computer game':0.9,
#                                                         'play station':0.5,
#                                                         'xbox':0.5})
# programming = PageTest(name='programming', knowledgeTokens={'programming language':0.6,
#                                                         'coding':0.8,
#                                                         'python':0.3})
#
# pageList = [electronicStore, movieReviews, videoGames, programming]
#
# for page in pageList:
#     page.add_shadow_tokens()
#     print(page.name)
#     print(f'\t\t{page.knowledgeTokens}')
#
#     plt.bar(page.knowledgeTokens.keys(),
#             page.knowledgeTokens.values())
#     plt.title(f'{page.name}')
#     plt.xlabel('Tokens')
#     plt.ylabel('Score')
#     plt.show()


# class Token():
#     """ Token has name and points to related tokens with weights """
#
#     def __init__(self, name):
#         self.name = name
#         self.value = 0
#         self.relatedTokens = []
#
#     def add_relatedToken(self, relatedToken, edgeWeight):
#         self.relatedTokens.append((edgeWeight, relatedToken))
#
#     def sort_relatedTokens(self):
#         self.relatedTokens.sort(reverse=True)
#
#     def increment_value(self, i):
#         self.value += i
#
#
# avgMax = 0
# n = 5
#
# for i, val in enumerate(corrDict.values()):
#     topThree = val[:n]
#     topScores = [elt[0] for elt in topThree]
#     scoreAvg = np.sum(topScores) / n
#     avgMax += scoreAvg
#
# avgMax /= i
#
# print(f'Avg: {avgMax}')
#
#
#
#
# tokenList = []
# for token, relatedTokens in corrDict.items():
#     curToken = Token(token)
#     for weight, related in relatedTokens:
#         curToken.add_relatedToken(related, weight)
#         curToken.sort_relatedTokens()
#     if token == 'coffee':
#         curToken.increment_value(0.5)
#     else:
#         curToken.increment_value(0.0625)
#     tokenList.append(curToken)
#
# allocDict = dict()
# for _ in range(10):
#     for token in tokenList:
#         # increment value if it has some
#         if token.name in allocDict:
#             avgScore = np.average(allocDict[token.name]) / len(allocDict[token.name])
#             _ = allocDict.pop(token.name)
#             token.increment_value(avgScore)
#         # calc allocations
#         outPower = np.sum([elt[0] for elt in token.relatedTokens])
#         tokenScore = token.value
#         curAllocs = {relatedToken: (tokenScore * (relatedScore / outPower))
#                         for relatedScore, relatedToken in token.relatedTokens}
#         for relatedToken, relatedScore in curAllocs.items():
#             if relatedToken in allocDict:
#                 allocDict[relatedToken].append(relatedScore)
#             else:
#                 allocDict.update({relatedToken: [relatedScore]})
#
#         # newAllocs = {relatedToken: (token.value * (int(relatedScore) / outPower))
#         #                 for relatedScore, relatedToken in token.relatedTokens}
#         # allocDict.update(newAllocs)
#         # print(token.value)
#
# for token in tokenList:
#     print(f'{token.name}: {token.value}')
