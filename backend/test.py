# import models.knowledge.knowledgeFinder as knowledgeFinder
# import models.knowledge.knowledgeBuilder as knowledgeBuilder
# import searchers.fuzzyMatcher as fuzzyMatcher
# from dataStructures.objectSaver import load
# from dataStructures.thicctable import Thicctable
# from models.processing.cleaner import clean_text, clean_url
# from crawlers.crawler import scrape_urlList
# import os
# from dataStructures.simpleStructures import Simple_List
# from searchers.databaseSearcher import or_search
# from models.processing.cleaner import clean_wiki
import re

def bold_tokens(tokenList, text, windowSize=40):
    """ Puts <strong></strong> around all  """
    # create matcher for all tokens in tokenList
    tokenString = "|".join(tokenList)
    # find list position of all starting locs of tokens in text
    locList = [elt.span()[0] for elt in re.finditer(tokenString, text)]

    def best_loc(locList):
        """
        Finds the number of tokens that start within windowSize of each loc.
        Returns loc with most tokens
        """
        # iterate over starting locations in locList
        for start in locList:


    print(locList)
    for loc in locList:
        print(loc)
        qualCount = 0
        for other in locList:
            print(f'\t{loc}')
            if other in range(loc, loc+1):
                qualCount += 1
                print('yes')
    # sub token matches for token surrounded by <strong> tags
    boldedText = re.sub(f"(?P<token>{tokenString})", "<strong>\g<token></strong>", text)

    return boldedText


test = 'hi how is harvard'
print(bold_tokens(['harvard', 'hi'], test))

# with open('data/inData/wikiTitles.txt') as knowledgeData:
    # for line in knowledgeData:
    #     # if (re.compile(r'[0-9]')).match(line):
    #     clean = clean_wiki(line)
    #     if 'dr dre' in clean:
    #         print(line,end='')
    #         print(f"\t{clean_wiki(line)}")

## Document vectorization ##
# from flashtext import KeywordProcessor
# from gensim.models.doc2vec import Doc2Vec
#
# knowledgeSet = {'harvard'}
#
# knowledgeProcessor = knowledgeBuilder.build_knowledgeProcessor(knowledgeSet)
#
# db = Thicctable(knowledgeSet)
#
# imdbModel = Doc2Vec.load('data/outData/binning/imdbModel.sav')
#
# urlList = ['www.harvard.edu', 'https://en.wikipedia.org/wiki/Harvard_University',
#             'https://simple.wikipedia.org/wiki/Harvard_University',
#             'https://twitter.com/Harvard?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor',
#             'https://twitter.com/HarvardHBS?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor',
#             'https://www.hbs.edu/Pages/default.aspx', 'http://www.harvard.com',
#             'https://www.allrecipes.com/recipes/76/appetizers-and-snacks/?internalSource=hub%20nav&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202']
#
# urlList = [urlList[1], urlList[4], urlList[-1]]
#
# docDict = {}
#
# import numpy as np
#
# vecMatrix = np.zeros((len(urlList), 300))
#
# for i, url in enumerate(urlList):
#     try:
#         pageText = htmlAnalyzer.get_pageText(url)
#         pageVec = docVecs.vectorize_document(pageText, imdbModel)
#         docDict.update({url:pageVec})
#         vecMatrix[i] = np.asarray(pageVec)
#         print(f"COMPLETE: {url}")
#     except Exception as e:
#         print(e)
#
# import matplotlib.pyplot as plt
#
# dists1, dists2 = [], []
#
# for i, col in enumerate(vecMatrix.T):
#     dist1 = np.abs(col[0] - col[1])
#     dist2 = np.abs(col[0] - col[2])
#     print(f"{i} dist1: {dist1} dist2: {dist2}")
#     if dist1 <0.5 and dist2 < 0.5:
#         print(f'\t\t\t{i}')
#     dists1.append(np.abs(dist1))
#     dists2.append(np.abs(dist2))
#
# # docVecs.visualize_vecDict(docDict)
# plt.plot(dists1)
# plt.plot(dists2)
# plt.show()
#
#
# pass
