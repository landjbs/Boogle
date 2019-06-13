import models.knowledge.knowledgeFinder as knowledgeFinder
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
import numpy as np

small = Thicctable([i for i in range(10)])

large = Thicctable([np.random.randint(0,10) for _ in range(10)])

small.save("small.sav")
large.save("large.sav")
