import crawlers.htmlAnalyzer as ha
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeTokenizer import build_knowledgeProcessor
import models.binning.docVecs as dv
from dataStructures.objectSaver import load, save
from dataStructures.thicctable import Thicctable

# # knowledge set loaded
# knowledgeSet = list(load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set'))
# testData = Thicctable(knowledgeSet)
# print('Data Table Created')
# del knowledgeSet
# # load knowledgeProcessor
# knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
# print('Knowledge Processor Created')


# BOOGLE #
print(f"{'-'*40}\nWelcome to Boogle!\n{'-'*40}")
vecDict = {}
while True:
    try:
        url = input("Page URL: ")
        if not url=='vis':
            pageText = ha.get_pageText(url)
            cleanText = "".join(dv.vector_tokenize(pageText))
            docVec = dv.vectorize_document(cleanText, modelPath="models/binning/d2vModel.sav")
            vecDict.update({url:docVec})
        else:
            dv.visualize_docVecs(vecDict)
    except Exception as e:
        print(e)



# print(time.time())
#
# start = time.time()
# knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
# end = time.time()
#
# print(f"Time: {end - start}")
#
#
# while True:
#     url = input("URL: ")
#     try:
#         pageString = url_to_pageString(url)
#         pageInfo = ha.analyze_html(pageString)
#         title = pageInfo['title']
#         print(title)
#         print(find_knowledgeTokens(title, knowledgeProcessor))
#     except Exception as e:
#         print(e)
