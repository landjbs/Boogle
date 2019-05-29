import re
import pandas as pd
import crawlers.urlAnalyzer as urlAnalyzer

dmozDF = pd.read_csv("data/dmoz_domain_category.tab.tsv", sep="\t", names=["url", "path"])

urlList = list(dmozDF['url'])

dmozDF['url'] = urlAnalyzer.urlList_to_stringList(urlList)
