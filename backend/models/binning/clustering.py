"""
Implementation of clustering algorithms to find groupings in a list of
document vectors generated with the help of models/binning/docVecs.py.
These clusters are used to define bins within the value portion of the
topDict key-val store implemented in dataStructures/thicctable.py.
By creating a second key-val mapping within the keyword-oriented topDict,
I hope to allow a smaller database to provide more comprehensive search
results than simple keyword lookup-tables.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sys import path
path.append("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend")
import crawlers.htmlAnalyzer as ha
import docVecs as dv
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# number of dimensions in document vector
NUM_DIMS = 300
# list of urls to analyze
urlList = ["https://en.wikipedia.org/wiki/Yogurt",
            "https://www.epicurious.com/recipes/food/views/homemade-yogurt-395111",
            "https://en.wikipedia.org/wiki/Connecticut_River"]
# initialize matrix to store docVec for each url
vecList = []
# iterate through urls
for i, url in enumerate(urlList):
    # fetch page text
    pageText = ha.get_pageText(url)
    # preprocess page text
    cleanText = "".join(dv.vector_tokenize(pageText))
    # make docVec for cleanText
    docVec = dv.vectorize_document(cleanText, modelPath="d2vModel.sav")
    # insert docVec into vecMatrix
    docDict = dv.docVec_to_dict(docVec)
    vecList.append(docDict)

df = pd.DataFrame(vecList)

corrDf = df.corr()

print(corrDf)

plt.imshow(corrDf)
plt.show()








pass
