from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import smart_open # for opening documents
from warnings import simplefilter
import re
import multiprocessing
import matplotlib.pyplot as plt
import pandas as pd
from dataStructures.objectSaver import save, load

# ignore warnings
simplefilter("ignore")


def vector_tokenize(inStr):
    """
    Converts string to clean, lowercase list of tokens.
    Specifically intended for vectorization after knowledgeTokenization.
    """
    # lowercase inStr, filter out common stop words and numerics
    cleanStr = strip_numeric(remove_stopwords(inStr.lower()))
    # tokenize cleanStr by whitespace
    tokens = word_tokenize(cleanStr)
    return tokens


def train_d2v(data, path='d2v.model', max_epochs=100, vec_size=300, alpha=0.025):
    """
    Trains doc vectorization model on iterable of docs and saves model to path
    """
    print(f"\n{'-'*40}\nTraining '{path}' model:")

    # list mapping list of document tokens to unique integer tag
    tagged_data = [TaggedDocument(words=clean_tokenize(_d), tags=[str(i)]) for i, _d in enumerate(data)]
    print(f"\tData Tagged (length={len(tagged_data)})")

    # initialize cores for fast model training
    cores = multiprocessing.cpu_count()

    # initialize model
    model = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1,
                    workders=cores)

    # build vector of all words contained in tagged data
    model.build_vocab(tagged_data)
    print(f"\tVocab Built\n\tModel Training for {max_epochs} epochs")

    # train model for max_epochs
    for epoch in range(max_epochs):
        print(f'\t\tEpoch: {epoch}', end="\r")
        model.train(tagged_data,
                    # signify that tagged_data is what was used to build vocab
                    total_examples=model.corpus_count,
                    # signify that train is only called once for efficiency
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    # save model to path
    model.save(path)
    print(f"Model saved to '{path}'.\n{'-'*40}")


def vectorize_document(doc, modelPath="test.model"):
    """ Vectorizes document with d2v model stored at modelPath """
    # load saved model
    model= Doc2Vec.load("test.model")
    # tokenize input doc
    tokenizedDoc = nltk.tokenize.word_tokenize(doc.lower())
    # create document vector for tokenizedDoc
    docVector = model.infer_vector(tokenizedDoc)
    return docVector


def docVec_to_dict(docVec):
    """ Converts docVec to dict for easy df insertion """
    docDict = {i:scalar for i, scalar in enumerate(docVec)}
    return docDict








pass
