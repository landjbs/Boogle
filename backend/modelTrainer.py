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
            docList.append(pageText)
            count += 1
            print(f"Analyzing {count}", end="\r")

dv.
