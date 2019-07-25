import numpy as np
from os import listdir

from dataStructures.objectSaver import load

people = ['Luther Dickinson', 'T. Coraghessan Boyle', 'Georges Parfait Mbida Messi',
            'Jim Bohannon', 'Paula Raymond']

peopleVecs = []

def cluster_file_contents(filePath, n):
    vecDict = {}
    for i, file in enumerate(listdir(filePath)):
        if i > n:
            break
        pageList = load(f'{filePath}/{file}')
        for pageDict in pageList:
            if pageDict['title'].strip() in people:
                peopleVecs.append(pageDict['pageVec'])
            vecDict.update({pageDict['title']: pageDict['pageVec']})
