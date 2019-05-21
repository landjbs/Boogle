# def crawl(init):
#     assert (isinstance(init, str)), "Usage: Crawler must be initialized with string"
#

import urllib.request

u2 = urllib.request.urlopen('http://finance.yahoo.com/q?s=aapl&ql=1')

for lines in u2.readlines():
    print (lines)
