"""
Employs code from a variety of bakend subfolders to train models
designed in backend/models. Models are trained in the top level
and then sent down to data/outData for storage. A top level trainer
is helpful because it has access to all the subfolders of the backend
and no module packaging is necessary.
"""

from os import scandir
import pandas as pd
from termcolor import colored
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt

from dataStructures.objectSaver import save, load
from models.processing.cleaner import clean_text
# import models.binning.docVecs as docVecs
import models.knowledge.knowledgeBuilder as knowledgeBuilder


PATH = 'data/outData/dmozProcessed'


# folderNums = {folder:i for i, folder in enumerate(os.listdir(PATH))}

def vectorize_folder(folderPath, folderNum, n=None, outPath=None):
    """
    Uses docVecs to vectorize n documents from folderPath.
    Returns: dataframe of shape (1024 + 1, n) vectorized documents. The first
    1024 dimensions are BERT encodings, the last is the number associated with
    the folder.
    Saves dataframe to outPath if given.
    """
    # folderContents
    vecList = []
    # iterate over contents of the folder
    for i, file in enumerate(scandir(folderPath)):

        print(f'\t{i}', end="\r")

vectorize_files()


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
