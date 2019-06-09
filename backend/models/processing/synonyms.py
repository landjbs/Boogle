import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

print('imported')

syns = wordnet.synsets("war")
print(syns)
