import re
import pandas as pd
import crawlerClass

def clean_url(url):
    """ Add 'www.' or 'http://' URLs for crawler analysis """
    # cast url to string
    urlString = str(url)
    # check starts
    if urlString.startswith('http'):
        pass
    elif urlString.startswith("www"):
        urlString = "http://" + urlString
    else:
        urlString = "http://www." + urlString
    return urlString

dmozDF = pd.read_csv("data/dmoz_domain_category.tab.tsv", sep="\t", names=["url", "path"])

dmozDF['url'] = dmozDF['url'].apply(lambda url : clean_url(url))

errors = 0
urlList = list(dmozDF['url'])
for i, url in enumerate(dmozDF['url']):
    try:
        pageString = crawlerClass.url_to_string(url)
    except:
        print(f"ERROR: {url}")
        errors += 1
    print(f"\t{i} urls analyzed with {errors} errors", end="\r")
    if i > 10:
        break
