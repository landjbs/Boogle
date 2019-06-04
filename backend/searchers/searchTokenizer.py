# Converts searchString into weighted list of search tokens
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'models')))
sys.path.append(os.path.abspath(os.path.join('..', 'dataStructures')))

from categorizer.gensimTest import clean_tokenize
