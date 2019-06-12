import models.binning.docVecs as dv
import os

#  584156 URLs analyzed with 396544 errors!

PATH = 'data/outData/dmozProcessed'
# iterable of pageTexts for training on
docList = []
count = 0

for folder in os.listdir(PATH):
    for file in os.listdir(f"{PATH}/{folder}"):
        with open(f"{PATH}/{folder}/{file}", 'r') as oldFile:
            pageText = oldFile.read()
            with open(f"{PATH}/All/{file}", 'w+') as newFile:
                newFile.write(pageText)
            count += 1
            print(f"Analyzing {count}", end="\r")

dv.train_d2v(docList, path="models/binning/d2vModel.sav")
