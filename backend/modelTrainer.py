"""
Employs code from a variety of bakend subfolders to train models
designed in backend/models. Models are trained in the top level
and then sent down to data/outData for storage. A top level trainer
is helpful because it has access to all the subfolders of the backend
and no module packaging is necessary.
"""

import models.binning.docVecs as dv
import os
import pandas as pd
from dataStructures.objectSaver import save, load
from models.processing.cleaner import clean_text
from keras.utils import to_categorical
import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np

from bert_serving.client import BertClient
bc = BertClient()

#  584156 URLs analyzed with 396544 errors!

PATH = 'data/outData/dmozProcessed'

vecList = []

def encode_folder(folderPath, folderNum, n):
    folderList = []
    for i, file in enumerate(os.listdir(folderPath)):
        if i > n:
            break
        with open(f'{folderPath}/{file}', 'r') as fileObj:
            try:
                text = fileObj.read()
                vec = bc.encode([text])[0]
                vecDict = {file:vec}
                # vecDict = dv.docVec_to_dict(vec)
                # vecDict = {0:0}
                # vecDict.update({'folder':folderNum})
                folderList.append(vecDict)
            except Exception as e:
                print(e)
            print(f'\t{i}', end="\r")
    print('\n')
    return folderList


def encode_folderList(topFolderPath):
    """ Uses BERT to encode files in folders under path """
    vecList = []

    for folder in os.listdir(topFolderPath):
        if not folder in ['.DS_Store', 'Kids_and_school', 'All']:
            print(folder)
            folderPath = f'{topFolderPath}/{folder}'
            if folder == 'Business':
                vecList += encode_folder(folderPath, 1, 3) #24111
            else:
                vecList += encode_folder(folderPath, 0, 3) #1854
    return vecList

vecList = encode_folderList(PATH)

docVecs = {}

for elt in vecList:
    docVecs.update(elt)

def score_doc(queryVec, docVec):
    score = np.sum(queryVec * docVec) / np.linalg.norm(docVec)
    return score

while True:
    query = input(colored('IN: ', 'red'))

    queryVec = bc.encode([query])[0]

    scoredDocs = [(doc, score_doc(queryVec, docVecs[doc])) for doc in docVecs]

    scoredDocs.sort(key=(lambda elt : elt[-1]), reverse=True)

    for i, doc in enumerate(scoredDocs):
        print(colored(doc[1], 'blue'), end='> ')
        print(colored(doc[0], 'cyan'), end='\n')
        if i > 5:
            break

# vecDF = pd.DataFrame(vecList)
#
# vecDF.to_csv('data/outData/binning/trainingVecsBERT.csv')

# vecDF = pd.read_csv('data/outData/binning/trainingVecsBERT.csv', sep=',')
