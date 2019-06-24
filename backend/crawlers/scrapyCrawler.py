import scrapy
import langid # to classify language of pageString
from bs4 import BeautifulSoup # to parse html


class CrawlerSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        """ Uses htmlAnalyzer.py to parse scrapy response """



# create soup object for parsing pageString
curSoup = BeautifulSoup(rawString, 'html.parser')
# pull title and text from soup object
title = (curSoup.title.string)
return title
# cleanedText, afterTitle = clean_pageText(curSoup.get_text(), title)
# cleanedTitle = clean_title(title)
#
# # validate language
# assert (detect_language(cleanedText)=='en'), f"{url} contents not in English"
#
# # find list of headers in soup object
# headerList = curSoup.find_all(headerMatcher)
# # join cleaned headers into space delimited string
# headers = " ".join(clean_text(str(header)) for header in headerList)
#
# # find contents of discription tag in soup object, if it exists
# try:
#     description = curSoup.find('meta', attrs={'name': 'description'}).get('content')
# except:
#     description = ""
#
# # find contents of keyword tag in soup object, if it exists
# try:
#     keywords = curSoup.find('meta', attrs={'name':'keywords'}).get('content')
# except:
#     keywords = ""
#
# # create dict of divs and contents for knowledge tokenization
# divDict = {'title':cleanedTitle, 'headers':headers, 'description':clean_text(description), 'keywords':clean_text(keywords),'all':cleanedText}
#
# # find dict mapping knowledge tokens in divDict to their score
# knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)
#
# # find and clean list of links from soup object
# linkList = list(map(lambda url : urlAnalyzer.fix_url(url), get_links(curSoup)))
#
# # decide text to use for window display; description if possible
# windowText = description if (description != "") else afterTitle
#
# # DOC VEC BELOW
# pageVec = docVecs.vectorize_document(cleanedText, d2vModel)
#
# # return list of information about the page
# return [cleanedTitle, knowledgeTokens, pageVec, linkList, windowText]
