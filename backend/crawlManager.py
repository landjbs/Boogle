from os import listdir

from crawlers.crawler import scrape_urlList
from crawlers.htmlAnalyzer import scrape_url

from models.knowledge.knowledgeBuilder import build_knowledgeProcessor

# urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[1000:40000]))
urlList = ['https://www.thecrimson.com/article/2019/6/25/sullivan-nyt-op-ed/',
            'https://www.thecrimson.com/article/2019/6/21/agassiz-family-says-give-up-photos/',
            'https://www.thecrimson.com/article/2019/6/27/bossi-end-of-the-world/',
            'https://fortnite.gamepedia.com',
            'https://www.wikipedia.org',
            'www.harvard.edu',
            'https://en.wikipedia.org/wiki/Harvard_University',
            'https://www.npr.org/sections/goatsandsoda/2019/06/27/736574110/study-u-s-ban-on-aid-to-foreign-clinics-that-promote-abortion-upped-abortion-rat']

knowledgeProcessor = build_knowledgeProcessor({'test'})

for url in urlList:
    try:
        scrape_url(url, knowledgeProcessor, {})
    except Exception as e:
        print(e)
