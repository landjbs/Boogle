import matplotlib.pyplot as plt
from bert_serving.client import BertClient
from termcolor import colored
import numpy as np
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from models.knowledge.knowledgeFinder import find_rawTokens
import re
from scipy.spatial.distance import euclidean

print(colored('Imports complete', 'cyan'))

bc = BertClient(check_length=False)

print(colored('Bert Config', 'cyan'))

knowledgeSet = {'how', 'to', 'do', 'python', 'list', 'comprehension', 'in', 'iceland'}

knowledgeProcessor = build_knowledgeProcessor(knowledgeSet)


document = 'how to do python list comprehension in iceland'

baseVec = bc.encode([document])[0]

# iteratively mask tokens
foundTokens = find_rawTokens(document, knowledgeProcessor)

scoreDict = {}

maskToken = '<MASK>'

for token in foundTokens:
    print(colored(f'\t{token}', 'red'), end=' | ')
    tempDoc = re.sub(token, maskToken, document)
    print(f'\t{tempDoc}')
    tempVec = bc.encode([tempDoc])[0]
    dist = euclidean(baseVec, tempVec)
    print(colored(dist, 'green'))
    scoreDict.update({token:dist})

plt.bar(scoreDict.keys(), scoreDict.values())
plt.ylabel('Euclidean Distance from Base Vector')
plt.title(f'Tokens Iteratively Replaced With "{maskToken}"')
plt.show()

# def score_doc(queryVec, docVec):
#     score = np.sum(queryVec * docVec) / np.linalg.norm(docVec)
#     return score
