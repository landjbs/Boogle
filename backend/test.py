import models.knowledge.knowledgeBuilder as knowledgeBuilder

knowledgeSet = knowledgeBuilder.build_knowledgeSet('data/inData/wikiTitles.txt',
                                                    "data/outData/knowledgeSet.sav")

while True:
    text = input("Search: ")
    print(f"Result: {text in knowledgeSet}")
