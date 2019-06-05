from gensim.parsing.preprocessing import remove_stopwords, strip_numeric
from nltk.tokenize import word_tokenize
sys.path.append(os.path.abspath(os.path.join('..', 'knowledgeClassifier')))

print(gensim.parsing.preprocessing.STOPWORDS)


# def possible_tokens(token):

def clean_tokenize(inStr):
    """ Converts string to clean, lowercase list of tokens """
    # lowercase inStr, filter out common stop words and numerics
    cleanStr = strip_numeric(remove_stopwords(inStr.lower()))
    # tokenize cleanStr by whitespace
    tokens = word_tokenize(cleanStr)
    return tokens
