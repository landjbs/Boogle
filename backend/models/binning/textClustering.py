import numpy as np
from os import listdir
from scipy.spatial.distance import euclidean

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
            title, vec = pageDict['title'].strip(), pageDict['pageVec']
            if title in people:
                peopleVecs.append(vec)
            vecDict.update({title: vec})

    peopleAverage = np.average(peopleVecs, axis=0)
    print(peopleAverage)
    rankedList = []
    for title, vec in vecDict.keys():
        if not title in people:
            distance = euclidean(vec, peopleAverage)
            rankedList.append((distance, title))
    rankedList.sort()

    for elt in rankedList:
        print(f'{elt[0]} - {elt[1]}')
