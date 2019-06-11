import models.knowledge.knowledgeTokenizer as knowledgeTokenizer

knowledgeSet = knowledgeTokenizer.build_knowledgeSet('data/inData/wikiTitles.txt',
                                                    "data/outData/knowledgeSet.sav")

while True:
    text = input("Search: ")
    print(f"Result: {text in knowledgeSet}")
