import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from dataStructures.objectSaver import save, load

with open("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/inData/frequencyData.csv") as FileObj:
    for word in FileObj:
        print(word)
