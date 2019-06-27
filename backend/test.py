import matplotlib.pyplot as plt
from bert_serving.client import BertClient
print('imports')
bc = BertClient()
print('bc')
vecList = []

while True:
    doc = input('In: ')
    if (doc=='PLOT'):
        plt.plot(vecList)
        plt.title('Document Vectors')
        plt.xlabel('Params')
        plt.ylabel('Values')
        plt.show()
    else:
        docVec = bc.encode([doc])
        vecList.append(docVec[0])
