"""
Employs code from a variety of bakend subfolders to train models
designed in backend/models. Models are trained in the top level
and then sent down to data/outData for storage. A top level trainer
is helpful because it has access to all the subfolders of the backend
and no module packaging is necessary.
"""

from searchers.modelBuilders.questionAnsweringModel import train_answering_lstm

train_answering_lstm('data/outData/searchAnalysis/squadDataFrames',
            outPath='data/outData/searchAnalysis/quetsionAnsweringModels.sav')


from os import listdir
import pandas as pd
from termcolor import colored
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt

from dataStructures.objectSaver import save, load
from models.processing.cleaner import clean_text
import models.knowledge.knowledgeBuilder as knowledgeBuilder
# import models.binning.docVecs as docVecs


PATH = 'data/outData/dmozProcessed'


# folderNums = {folder:i for i, folder in enumerate(os.listdir(PATH))}

def vectorize_folder(folderPath, folderNum, n=None):
    """
    Uses docVecs to vectorize n documents from folderPath.
    Returns: list of dicts of shape (1024 + 1, n) vectorized documents. The first
    1024 dimensions are BERT encodings, the last is the number associated with
    the folder.
    """
    # list of files in folderPath
    fileList = listdir(folderPath)
    if not n:
        n = len(fileList)
    vecList = []
    folderDict = {'folder':folderNum}
    # iterate over contents of the folder, coverting files to dicts of BERT scalars
    for i, file in enumerate(fileList):
        if i >= n:
            break
        try:
            with open(f'{folderPath}/{file}', 'r') as fileObj:
                fileDict = {'file':file}
                text = fileObj.read()
                if text=="":
                    pass
                else:
                    vector = docVecs.vectorize_all(text)
                    fileDict = docVecs.vec_to_dict(vector)
                    fileDict.update(folderDict)
                    vecList.append(fileDict)
        except Exception as e:
            print(f"ERROR: {e}")
        print(f'\t{i}', end="\r")
    return vecList

def vectorize_top_folder(topPath, excludeFolders=['.DS_Store', 'All'], outPath=None):
    """
    Vectorizes all folders in topPath, except for those in excludeFolders.
    Returns: dataframe of shape (1024 + 1, n) vectorized documents.
    Saves to outPath if specified.
    """
    # get dict mapping non-excluded folders in topPath to unique int
    folderNums = {folder:i for i, folder in enumerate(listdir(topPath)) if not folder in excludeFolders}
    # iterate over folders, builing list of vectorized files
    vecList = []
    for folder, folderNum in folderNums.items():
        print(folder)
        vecList += vectorize_folder(f'{topPath}/{folder}', folderNum, 1000)
        print('\n')
    # convert vecList to dataframe and save to outPath if given
    vecDF = pd.DataFrame(vecList)
    if outPath:
        vecDF.to_csv(outPath)
        print(f"Dataframe saved to '{outPath}'.")
    return vecDF

print(vectorize_top_folder("data/outData/dmozProcessed", outPath='data/outData/binning/vecNames.sav'))


# def encode_folder(folderPath, folderNum, n):
#     folderList = []
#     for i, file in enumerate(os.listdir(folderPath)):
#         if i > n:
#             break
#         with open(f'{folderPath}/{file}', 'r') as fileObj:
#             try:
#                 text = fileObj.read()
#                 vec = bc.encode([text])[0]
#                 vecDict = dv.docVec_to_dict(vec)
#                 vecDict.update({'folder':folderNum})
#                 folderList.append(vecDict)
#             except Exception as e:
#                 print(e)
#             print(f'\t{i}', end="\r")
#     print('\n')
#     return folderList
#
#
# def encode_folderList(topFolderPath):
#     """ Uses BERT to encode files in folders under path """
#     vecList = []
#
#     for folder in os.listdir(topFolderPath):
#         if not folder in ['.DS_Store', 'Kids_and_school', 'All']:
#             print(folder)
#             folderPath = f'{topFolderPath}/{folder}'
#             if folder == 'News':
#                 vecList += encode_folder(folderPath, 1, 300)
#             else:
#                 vecList += encode_folder(folderPath, 0, 23)
#     return vecList
#
#
#
#
#
#
#
#
# pass
