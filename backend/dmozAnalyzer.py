import re
import pandas as pd
import crawlers.urlAnalyzer as ua

dmozDF = pd.read_csv("data/dmoz_domain_category.tab.tsv", sep="\t", names=["url", "path"])

dmoz_urlList = list(dmozDF["url"])

dmozDF["pageString"] = ua.urlList_to_stringList(dmoz_urlList)

dmozDF.to_csv("data/dmoz.tab.tsv", sep='\t')
