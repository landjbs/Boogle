import models.knowledge.knowledgeFinder as knowledgeFinder
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable

db = Thicctable({'test'})

db.insert_value('test','bool juice')

db.add_key('test2')

db.insert_value('test2', 'jyce man')

db.insert_value('test2', 'jyce woman')

db.save('test.savv')
