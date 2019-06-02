import pickle
from dataStructures.simpleStructures import Simple

test = Simple()

test.add(5)

test.add(4)

file = open('test.obj', 'wb')

pickle.dump(test, file)

file.close()

# revive
filehandler = open("test.obj", 'rb')
object = pickle.load(filehandler)

print(object)

print(object.data)
