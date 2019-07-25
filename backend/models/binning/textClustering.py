from os import listdir

from dataStructures.objectSaver import load

def cluster_file_contents(filePath):
    vecDict = {}

    for i, file in enumerate(listdir(filePath)):
        pageList = load(f'{filePath}/{file}')
        for pageDict in pageList:
            vecDict.update({pageDict['title']: pageDict['pageVec']})

            print(vecDict)
