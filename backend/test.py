import zlib
from dataStructures.objectSaver import save
import json


testDict = {'a':(1,2,3) for _ in range(1000000)}

save(testDict, 'uncompressed')

dicstring = json.dumps(testDict)
print(dicstring)
compressed = zlib.compress(dicstring, 9)

save(compressed, 'compressed')
