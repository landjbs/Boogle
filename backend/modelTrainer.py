import models.binning.docVecs as dv
import smart_open
import os


PATH = 'data/outData/dmozProcessed'
# iterable of pageTexts for training on
docList = []
count = 0

for folder in os.listdir(PATH):
    for file in os.listdir(f"{PATH}/{folder}"):
        with open(f"{PATH}/{folder}/{file}", 'r') as fObj:
            pageText = fObj.read()
            cleanText = "".join(dv.vector_tokenize(pageText))
            print(cleanText)
            docList.append(cleanText)
            count += 1
            print(f"Analyzing {count}", end="\r")

dv.train_d2v(docList, path="models/binning/d2vModel.sav")
