import re
import hmtlAnalyzer
import crawlerClass
import numpy as np
import pandas as pd

"""

Features:

"""

dmozMatrix = np.read_csv("../outputs/dmoz_domain_category.tab.tsv", delimiter="\t")

for url, path in dmozMatrix:
    pageString = crawlerClass.url_to_string(url)
