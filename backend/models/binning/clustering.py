"""
Implementation of clustering algorithms to find groupings in a list of
document vectors generated with the BERT model in models/binning/docVecs.py.
These clusters are used to define bins within the value portion of the
topDict key-val store implemented in dataStructures/thicctable.py.
By creating a second key-val mapping within the keyword-oriented topDict,
I hope to allow a smaller database to provide more comprehensive search
results than simple keyword lookup-tables.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import crawlers.htmlAnalyzer as ha
import docVecs as dv
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE









pass
