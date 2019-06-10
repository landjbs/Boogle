import crawlers.htmlAnalyzer as ha
from models.processing.cleaner import clean_text
from dataStructures.thicctable import Thicctable
from models.knowledge.knowledgeTokenizer import build_knowledgeProcessor
from dataStructures.objectSaver import load, save

# # knowledge set loaded
knowledgeSet = list(load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set'))
# testData = Thicctable(knowledgeSet)
# print('Data Table Created')
# del knowledgeSet
# # load knowledgeProcessor
# knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
# print('Knowledge Processor Created')


# BOOGLE #
print(f"{'-'*40}\nWelcome to Boogle!\n{'-'*40}")
while True:
    # try:
    url = input("Page URL: ")
    pageList = ha.scrape_url(url) #knowledgeProcessor
    print("\t\tSearch Results")
    for elt in pageList:
        print(elt, end=f"\n{'-'*50}\n")
    except Exception as e:
        print(f"\t\tERROR: {e}")


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
