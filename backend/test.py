# from models.knowledge.knowledgeFinder import find_scoredTokens

filePath = 'data/inData/wikipedia_utf8_filtered_20pageviews.csv'

with open(filePath, 'r') as wikiCsv:
    for i, line in enumerate(wikiCsv):
        if i < 100:
            # get everything after the first comma
            rawText = line[21:]
            titleEnd = rawText.find('  ')
            title = rawText[:titleEnd]
            articleText = rawText[(titleEnd+2):]
            articleText = articleText.strip()
            divDict = {}
