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

#  584156 URLs analyzed with 396544 errors!

PATH = 'data/outData/dmozProcessed'

# for folder in os.listdir(PATH):
#     print(folder)
#     for i, file in enumerate(os.listdir(f"{PATH}/{folder}")):
#         if i < 10:
#             with open(f"{PATH}/{folder}/{file}", 'r') as oldFile:
#                 pageText = oldFile.read()
#                 with open(f"{PATH}/All/{file}", 'w+') as newFile:
#                     newFile.write(pageText)
#                 print(f"Analyzing {i}", end="\r")
#         else:
#             break


dv.train_d2v(folderPath="data/outData/dmozProcessed/All",
            outPath="data/outData/binning/d2vModel.sav")

folderNums = {folder:i for i, folder in enumerate(os.listdir(PATH))}
print(folderNums)

model = dv.load_model('data/outData/binning/d2vModel.sav')

dataList = []

for folder in os.listdir(PATH):
    if folder not in ['.DS_Store', 'All']:
        print(folder)
        for i, file in enumerate(os.listdir(f"{PATH}/{folder}")):
            if i < 100:
                with open(f"{PATH}/{folder}/{file}", 'r') as oldFile:
                    text = clean_text(oldFile.read())
                    vec = dv.vectorize_document(text, model)
                    vecDict = docVec_to_dict(vec)
                    fileDict = vecDict.update('folder':folderNums[folder])
                    dataList.append(fileDict)

df = pd.DataFrame(dataList)

print(df)

load(df, 'folderVecs.sav')

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical

model = Sequential([
    Dense(300, input_shape=(300,)),
    Activation('relu'),
    Dense(15),
    Activation('softmax'),
])

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

trainDF = df.copy()
trainDF.drop("folder",axis=1)

model.fit(trainDF, to_categorical(df['folder']), epochs=10)

model.save('data/outData/binning/classificationModel.sav')
