"""
Modified pageRank testing
"""

import numpy as np
from collections import Counter
from scipy.special import softmax

class Token():
    """ Token has name and points to related tokens with weights """

    def __init__(self, name):
        self.name = name
        self.value = 0
        self.relatedTokens = []

    def add_relatedToken(self, relatedToken, edgeWeight):
        self.relatedTokens.append((edgeWeight, relatedToken))

    def sort_relatedTokens(self):
        self.relatedTokens.sort(reverse=True)

    def increment_value(self, i):
        self.value += i


corrDict ={'coffee': [(471369940.24214125, 'espresso'), (238482974.2349554, 'dunkin donuts'), (136305343.318782, 'starbucks'), (1030891.7330982436, 'residue'), (697518.602966686, 'wood'), (378287.75076798926, 'cabin'), (178624.0879016093, 'logs')], 'residue': [(2924918.270165199, 'wood'), (2323922.4675443554, 'espresso'), (1030891.7330982436, 'coffee'), (509154.1399538477, 'logs'), (148079.61646287164, 'cabin'), (6719.840195308946, 'starbucks')], 'wood': [(10545018.46488576, 'logs'), (2924918.270165199, 'residue'), (966576.846654676, 'cabin'), (697518.602966686, 'coffee'), (300048.34970461705, 'starbucks'), (229798.86926247875, 'espresso'), (114394.80896480675, 'dunkin donuts')], 'logs': [(15274336.302278876, 'cabin'), (10545018.46488576, 'wood'), (509154.1399538477, 'residue'), (178624.0879016093, 'coffee'), (151672.60268078465, 'starbucks'), (29784.687969318722, 'espresso')], 'cabin': [(15274336.302278876, 'logs'), (966576.846654676, 'wood'), (378287.75076798926, 'coffee'), (262194.87612188945, 'starbucks'), (148079.61646287164, 'residue'), (91408.92232100834, 'espresso')], 'starbucks': [(244032123.67514265, 'espresso'), (136305343.318782, 'coffee'), (42907255.156458475, 'dunkin donuts'), (300048.34970461705, 'wood'), (262194.87612188945, 'cabin'), (151672.60268078465, 'logs'), (6719.840195308946, 'residue')], 'espresso': [(471369940.24214125, 'coffee'), (244032123.67514265, 'starbucks'), (10703821.033933356, 'dunkin donuts'), (2323922.4675443554, 'residue'), (229798.86926247875, 'wood'), (91408.92232100834, 'cabin'), (29784.687969318722, 'logs')], 'dunkin donuts': [(238482974.2349554, 'coffee'), (42907255.156458475, 'starbucks'), (10703821.033933356, 'espresso'), (114394.80896480675, 'wood')]}

tokenList = []
for token, relatedTokens in corrDict.items():
    curToken = Token(token)
    for weight, related in relatedTokens:
        curToken.add_relatedToken(related, weight)
        curToken.sort_relatedTokens()
    if token == 'coffee':
        curToken.increment_value(0.5)
    elif token == 'logs':
        curToken.increment_value(0.5)
    else:
        curToken.increment_value(0.0000001)
    tokenList.append(curToken)

allocDict = Counter()
for _ in range(10):
    for token in tokenList:
        # increment value if it has some
        if token.name in allocDict:
            curAlloc = allocDict.pop(token.name)
            token.increment_value(curAlloc)
        # calc allocations
        outPower = np.sum([elt[0] for elt in token.relatedTokens])
        tokenScore = token.value
        allocPower = {relatedToken: (tokenScore * (relatedScore / outPower))
                        for relatedScore, relatedToken in token.relatedTokens}
        allocDict.update(allocPower)

        # newAllocs = {relatedToken: (token.value * (int(relatedScore) / outPower))
        #                 for relatedScore, relatedToken in token.relatedTokens}
        # allocDict.update(newAllocs)
        # print(token.value)

for token in tokenList:
    print(f'{token.name}: {token.value}')
