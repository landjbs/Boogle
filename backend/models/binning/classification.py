"""
Loads and applies classification models to bucket pages based on
BERT vector
"""

import pandas as pd # to format document vectors for classification
from keras.models import load_model # to classify document vectors

newsClassifier = load_model('data/outData/binning/newsClassifier.sav')

def classify_page(pageVec):
    """
    Returns category of page from dataframe of docVec.
    Currently classifies 'News' or 'Other'
    """
    # enocde vec as pandas dataframe
    vecDF = pd.DataFrame(docVec_to_dict(pageVec))
    # run classifier on vecDF
    newsScore = newsClassifier.predict(vecDF)
    category = 'News' if newsScore > 0.8 else 'Other'
    return category
