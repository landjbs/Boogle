# Script responsible for returning processed data from HTML pageString
# passed from urlAnalyzer. Outsources all NLP and ML to backend/models.

import re
import datetime # to find the loadTime of a page
from bs4 import BeautifulSoup
import urllib.request
import urlAnalyzer as ua

# matcher for text in <title></title> tags, ignoring case
titleString = r'(?<=<title>).+(?=</title>)'
titleMatcher = re.compile(titleString, re.IGNORECASE)

# matcher for links denoted by https:// or http://
linkString = r'https://\S+(?=")|http://\S+(?=")'
linkMatcher = re.compile(linkString)

# matcher for everything in <body...></body> tags
bodyString = r'(?<=<body).+(?=</body>)'
bodyMatcher = re.compile(bodyString)

# image string
imageString = '(?<=src=")' + "\S+" + '(?=")'
imageMatcher = re.compile(imageString)

# text = '<body>Hi</body>'
# x = bodyMatcher.findall(text)
# print(x)

# url = "https://www.harvard.edu/"
#
# pageString = ua.url_to_string(url)

with open('../data/practiceWeb.txt', 'r') as FileObj:
    text = "".join(line for line in FileObj)

soup = BeautifulSoup(text, "html.parser")

one_a_tag = soup.findAll('a')[36]
link = one_a_tag['href']

print(link)
