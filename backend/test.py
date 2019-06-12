import models.knowledge.knowledgeFinder as knowledgeFinder
from dataStructures.objectSaver import load


knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')

test = load('data/outData/knowledge/freqDict.sav')

while True:
    div = input("Div: ")
    text = input("Text: ")
    divDict = {div:text}
    print(knowledgeFinder.score_divDict(divDict, knowledgeProcessor))
