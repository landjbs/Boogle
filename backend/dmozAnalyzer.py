import re
import pandas as pd
import crawlers.urlAnalyzer as ua
import time


dmozDF = pd.read_csv("data/test.tab.tsv", sep="\t", names=["url", "path"])

dmoz_urlList = list(dmozDF["url"])

start = time.time()

testOut = ua.scrape_urlList(dmoz_urlList, workerNum=50)

end = time.time()

print(f"Process Complete!\nURLs analyzed in {end-start} seconds!")
