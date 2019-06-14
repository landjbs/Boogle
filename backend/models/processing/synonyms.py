import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

print('imported')

while True:
    search = input("Search: ")
    print(wordnet.synsets(search))
