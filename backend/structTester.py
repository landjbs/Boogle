from dataStructures.scrapingStructures import SaverQueue

x = SaverQueue('h', 5)

for i in range(3):
    x.add(i)
    print(x.data)
