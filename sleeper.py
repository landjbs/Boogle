import time
import numpy as np

def gen_string():
    # create uniform dist of ints across ascii hexes
    raw_ints = np.random.randint(33,127, 30)
    # map hex to ascii and int chars
    cList = list(map(lambda i : chr(i), raw_ints))
    iList = list(map(lambda i : str(i), raw_ints))
    # create strings for cList and i List
    cOut = "".join(cList)
    iOut = "".join(iList)
    # create and return outstr
    outStr = cOut + ": " + iOut
    return outStr

def gen_rand():
    while True:
        print(gen_string())
        if np.random.randint(0,60)==30:
            print('-'*60)
        time.sleep(np.random.uniform(0.01, 0.5))

gen_rand()
