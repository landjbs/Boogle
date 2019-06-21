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
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.utils import to_categorical
import matplotlib.pyplot as plt

#  584156 URLs analyzed with 396544 errors!

PATH = 'data/outData/dmozProcessed'
#
# for folder in os.listdir(PATH):
#     print(folder)
#     for i, file in enumerate(os.listdir(f"{PATH}/{folder}")):
#         if i < 1000:
#             with open(f"{PATH}/{folder}/{file}", 'r') as oldFile:
#                 pageText = oldFile.read()
#                 with open(f"{PATH}/All/{file}", 'w+') as newFile:
#                     newFile.write(pageText)
#                 print(f"Analyzing {i}", end="\r")
#         else:
#             break
#
#
# dv.train_d2v(folderPath="data/outData/dmozProcessed/All",
#             outPath="data/outData/binning/d2vModel.sav")

#
# folderNums = {folder:i for i, folder in enumerate(os.listdir(PATH))}
# print(folderNums)
#
# model = dv.load_model('data/outData/binning/d2vModel.sav')
#
# dataList = []
# for folder in os.listdir(PATH):
#     if folder not in ['.DS_Store', 'All', 'News']:
#         print(folder)
#         for i, file in enumerate(os.listdir(f"{PATH}/{folder}")):
#             if i < 1000n:
#                 with open(f"{PATH}/{folder}/{file}", 'r') as oldFile:
#                     text = clean_text(oldFile.read())
#                     vec = dv.vectorize_document(text, model)
#                     vecDict = dv.docVec_to_dict(vec)
#                     vecDict.update({'folder':0})
#                     dataList.append(vecDict)
#                     print(f"\tVectorizing: {i}", end="\r")
#             else:
#                 break
#
# for i, file in enumerate(os.listdir("data/outData/dmozProcessed/News")):
#     if i < 14000:
#         with open(f"data/outData/dmozProcessed/News/{file}") as f:
#             text = clean_text(f.read())
#             vec = dv.vectorize_document(text, model)
#             vecDict = dv.docVec_to_dict(vec)
#             vecDict.update({'folder':1})
#             dataList.append(vecDict)
#         print(f"\tVectorizing: {i}", end="\r")
#
# df = pd.DataFrame(dataList)
#
# print(df)
#
# folderScores = to_categorical(df['folder'])
# df = df.drop("folder", axis=1)
#
# print(df)
# save(df, 'data/outData/binning/binaryTrainingVecs.sav')
df = load('data/outData/binning/binaryTrainingVecs.sav')
described = df.describe()
std = described.loc['std']
plt.plot(std)
plt.show()

#
# model = Sequential([
#     Dense(300, input_shape=(300,)),
#     Activation('relu'),
#     Dense(60),
#     Activation('relu'),
#     Dense(2),
#     Activation('softmax'),
# ])
#
# model.compile(optimizer='rmsprop',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
#
# model.fit(df, folderScores, epochs=60)
#
# model.save('data/outData/binning/binaryModel.sav')


# import matplotlib.pyplot as plt
# classificationModel = load_model("data/outData/binning/binaryModel.sav")
#
# vectorizationModel = dv.load_model("data/outData/binning/d2vModel.sav")
# print('NEWS')
#
# newsList = [0,0]
#
# for i, file in enumerate(os.listdir(f"{PATH}/News")):
#     # print(i)
#     if i < 50:
#         with open(f"{PATH}/News/{file}") as f:
#             text = f.read()
#             vec = pd.DataFrame([dv.docVec_to_dict(dv.vectorize_document(text, vectorizationModel))])
#             predictions = classificationModel.predict(vec)
#             if predictions[0][0] < predictions[0][1]:
#                 print(file)
#             newsList[0] += (predictions[0][0])
#             newsList[1] += predictions[0][1]
# print(newsList)
# shoppingList = [0,0]
# print("Shopping")
# for i, file in enumerate(os.listdir(f"{PATH}/Shopping")):
#     if 1050 >i > 1000:
#         with open(f"{PATH}/Shopping/{file}") as f:
#             text = f.read()
#             vec = pd.DataFrame([dv.docVec_to_dict(dv.vectorize_document(text, vectorizationModel))])
#             predictions = classificationModel.predict(vec)
#             shoppingList[0] += (predictions[0][0])
#             shoppingList[1] += predictions[0][1]
# print(shoppingList)
# plt.show()
