from dataStructures.objectSaver import save
from os import listdir

urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')))

print(len(urlList))

save(urlList, "data/inData/urlList.sav")
