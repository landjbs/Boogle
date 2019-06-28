import matplotlib.pyplot as plt
from bert_serving.client import BertClient
from termcolor import colored
import numpy as np

print(colored('Imports complete', 'cyan'))

bc = BertClient(check_length=False)

print(colored('Bert Config', 'cyan'))

vecList = []

rawDocs = ['hi how are you on this beautiful day', 'i ran across the bridge over the river', 'my dog is getting fat but she is still cute']

docVecs = {doc:(bc.encode([doc])[0]) for doc in rawDocs}

def score_doc(queryVec, docVec):
    score = np.sum(queryVec * docVec) / np.linalg.norm(docVec)
    return score


while True:
    query = input(colored('IN: ', 'red'))
    if not (query==""):
        try:
            queryVec = bc.encode([query])[0]

            scoredDocs = [(doc, score_doc(queryVec, docVecs[doc])) for doc in docVecs]

            scoredDocs.sort(key=(lambda elt : elt[-1]), reverse=True)

            for i, doc in enumerate(scoredDocs):
                if not i > 5:
                    print(colored(doc[1], 'blue'), end='> ')
                    print(colored(doc[0], 'cyan'), end='\n')

            docVecs.update({query:queryVec})
        except Exception as e:
            print(f"ERROR: {e}")
