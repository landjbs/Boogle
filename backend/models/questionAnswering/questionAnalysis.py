import json_lines
import os
from models.knowledge.dependencyParser import get_entities
from dataStructures.clusterStruct import ClusterDict
import models.binning.docVecs as docVecs
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from dataStructures.objectSaver import load


# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
questionDict = {'india':[], 'fornite':[]}

files = os.listdir('data/inData/GoogleQuestions/natural_questions/v1.0/train')
print(files)
for file in files:
    if not file in ['.DS_Store'] and (len(questionDict['india'])<1000):
        with open(f'data/inData/GoogleQuestions/natural_questions/v1.0/train/{file}', 'rb') as f: # /nq-dev-sample.jsonl
           for i, item in enumerate(json_lines.reader(f)):
               print(f'\t{i}', end='\r')
               questionStr = (item['question_text'])
               if 'india' in questionStr:
                   # entities = knowledgeProcessor.extract_keywords(questionStr)
                   entities = list(map((lambda entity:entity[0]), get_entities(questionStr)))
                   # for elt in ['the', 'to', 'why', 'how', 'a', 'in', 'out', 'when', 'what', 'in', 'from']:
                   #     try:
                   #         entities.remove(elt)
                   #     except:
                   #         pass
                   for entity in entities:
                       if entity in questionDict:
                           print(questionStr)
                           questionDict[entity].append(questionStr)
                       else:
                           questionDict.update({entity:[questionStr]})
                       # firstAnswer = item['long_answer_candidates'][0]
                       # firstStart, firstEnd = firstAnswer['start_token'], firstAnswer['end_token']
                       # pageTokens = item['document_tokens']
                       # tokenList = [elt['token'] for elt in pageTokens]
                       # answerText = ' '.join(token for token in tokenList[firstStart:firstEnd])
                       # print(f'{questionStr}:\n\t{answerText}')
                       # print(f'{questionStr}: {}')
                       # print(f'\t{i}',end='\r')


searchDict = {}

knowledgeProcessor = build_knowledgeProcessor(questionDict.keys())

for token in questionDict:
    print(token.upper())
    questions = set()
    for elt in questionDict[token]:
        print(f'\t- {elt}')
        questions.add(elt)
    searchDict.update({token:ClusterDict(questions)})

while True:
    search = input('search: ')
    try:
        searchToken = (knowledgeProcessor.extract_keywords(search))[0]
        bucket = searchDict[searchToken]
        results = bucket.find_nearest_simple(search, n=2)
        print(f'{search}: {searchToken}')
        for result in results:
            print(f'\t- {result}')
    except Exception as e:
        print(f"ERROR: '{e}'")



# import spacy
# import textacy.extract
#
# # Load the large English NLP model
# nlp = spacy.load('en_core_web_lg')
#
# def parse_entities(text):
#     doc = nlp(text)
#     entityList = [entity.text for entity in doc.ents]
#     for entity in entityList:
#         # Extract semi-structured statements
#         statements = textacy.extract.semistructured_statements(doc, entity)
#         # Print the results
#         for statement in statements:
#             subject, verb, fact = statement
#             print(f"{subject} {verb} {fact}")
#
#
# with open('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'r') as wikiFile:
#     for i, line in enumerate(wikiFile):
#         parse_entities(line)

from dataStructures.clusterStruct import ClusterDict
from models.processing.cleaner import clean_text

wordSet = set()

with open('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'r') as wikiFile:
    for i, line in enumerate(wikiFile):
        if i < 100:
            cleanLine = clean_text(line)
            lineWords = cleanLine.split()
            for word in lineWords:
                wordSet.add(word)
            print(wordSet)
        print(f"Line: {i} | Num Words: {len(wordSet)}", end="\r")

from dataStructures.clusterStruct import ClusterDict
from models.processing.cleaner import clean_text

wordSet = set()

with open('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'r') as wikiFile:
    for i, line in enumerate(wikiFile):
        if i < 100:
            cleanLine = clean_text(line)
            lineWords = cleanLine.split()
            for word in lineWords:
                wordSet.add(word)
            print(wordSet)
        print(f"Line: {i} | Num Words: {len(wordSet)}", end="\r")

from dataStructures.clusterStruct import ClusterDict
from models.processing.cleaner import clean_text

wordSet = set()

with open('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'r') as wikiFile:
    for i, line in enumerate(wikiFile):
        if i < 100:
            cleanLine = clean_text(line)
            lineWords = cleanLine.split()
            for word in lineWords:
                wordSet.add(word)
            print(wordSet)
        print(f"Line: {i} | Num Words: {len(wordSet)}", end="\r")

from dataStructures.clusterStruct import ClusterDict
from models.processing.cleaner import clean_text

wordSet = set()

with open('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'r') as wikiFile:
    for i, line in enumerate(wikiFile):
        if i < 100:
            cleanLine = clean_text(line)
            lineWords = cleanLine.split()
            for word in lineWords:
                wordSet.add(word)
            print(wordSet)
        print(f"Line: {i} | Num Words: {len(wordSet)}", end="\r")

test = ClusterDict(wordSet)

while True:
    search = input('search: ')
    nearestWords = test.find_nearest(search)
    for i, word in enumerate(nearestWords):
        print(f'\t{i}: {word}')
