import models.knowledge.knowledgeFinder as knowledgeFinder
from dataStructures.objectSaver import load


knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
freqDict = load('data/outData/knowledge/freqDict.sav')

while True:
    div = input("Div: ")
    text = input("Text: ")
    try:
        divDict = {div:text}
        print(knowledgeFinder.score_divDict(divDict, knowledgeProcessor, freqDict))
    except Exception as e:
        print(e)
