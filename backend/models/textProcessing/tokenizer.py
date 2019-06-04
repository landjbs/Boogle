from gensim.parsing.preprocessing import remove_stopwords, strip_numeric

def clean_tokenize(inStr):
    """ Converts string to clean, lowercase list of tokens """
    # lowercase inStr, filter out common stop words and numerics
    cleanStr = strip_numeric(remove_stopwords(inStr.lower()))
    # tokenize cleanStr by whitespace
    tokens = nltk.tokenize.word_tokenize(cleanStr)
    return tokens
