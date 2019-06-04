# Converts searchString into weighted list of search tokens
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'models')))

from textProcessing.tokenizer import clean_tokenize


testSearch = input(f"Search: ")
