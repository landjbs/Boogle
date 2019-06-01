import pandas as pd
import crawlers.crawler as crawler
import time
import crawlers.urlAnalyzer as ua

dmozDF = pd.read_csv("data/test.tab.tsv", sep="\t", names=["url", "path"])

dmoz_urlList = list(dmozDF["url"])

start = time.time()

testOut = crawler.scrape_urlList(dmoz_urlList[80:90], workerNum=20)

end = time.time()

print(f"Process Complete!\n{len(testOut.data)} URLs analyzed in {end-start} seconds!")
