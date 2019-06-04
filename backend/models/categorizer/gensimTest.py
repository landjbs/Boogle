from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.parsing.preprocessing import remove_stopwords, strip_numeric
import nltk
from os import listdir # for
import smart_open # for opening documents
# ignore warnings
import warnings
warnings.simplefilter("ignore")
import re
import multiprocessing
import matplotlib.pyplot as plt
import pandas as pd
# model stuff
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical


def clean_tokenize(inStr):
    """ Converts string to clean, lowercase list of tokens """
    # lowercase inStr, filter out common stop words and numerics
    cleanStr = strip_numeric(remove_stopwords(inStr.lower()))
    # tokenize cleanStr by whitespace
    tokens = nltk.tokenize.word_tokenize(cleanStr)
    return tokens


def train_d2v(data, path='d2v.model', max_epochs=100, vec_size=300, alpha=0.025):
    """ Trains doc vectorization model on iterable of docs and saves model to path """
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


def visualize_docVecs(vecList):
    """ Plots list of docVecs to determine differences """
    for vec in vecList:
        plt.plot(vecList)
    plt.title(f'Vectors for {len(vecList)} Documents')
    plt.xlabel('Vector Dimensions')
    plt.ylable('Document Value')
    plt.show()


def scan_file(file, path):
    """ Scans file into contained pageText """
    FileObj = smart_open.open(f"{path}/{file}", 'r')
    pageText = "".join([line for line in FileObj])
    return pageText


def file_to_dict(file, filePath, modelPath, score):
    """ Converts file and stored path to dict with docVec and score"""
    text = scan_file(file, filePath)
    docVec = vectorize_document(text, modelPath=modelPath)
    docDict = docVec_to_dict(docVec)
    docDict.update({'score':score})
    return docDict


def genData(pathDict, numSamples=100, outPath=""):
    """
    Generates dataframe of text vectors and corresponding score from
    dict mapping path to score. Saves to outPath if given. Reads
    numSamples from each file.
    """
    dataList = []
    for path in pathDict:
        print(f"Analyzing {path}")
        files = listdir(path)
        fileDicts = [file_to_dict(file, path, "test.model", pathDict[path]) for i, file in enumerate(files) if i < numSamples]
        dataList += fileDicts
    df = pd.DataFrame(dataList)
    print(f"Dataframe of size {df.shape} generated")
    if not (outPath==""):
        df.save(outPath)
        print(f"Saved to {outPath}")
    return(df)

###### MODEL STUFF ######
# read train data from pathDict
trainDF = genData({'aclImdb/train/pos':1, 'aclImdb/train/neg':0})
# split train df into vecs and encoded scores
trainVecs = trainDF.copy()
trainVecs = trainVecs.drop('score', axis=1)
trainScores = to_categorical(trainDF['score'])

# read test data from pathDict
testDF = genData({'aclImdb/train/pos':1, 'aclImdb/train/neg':0}, numSamples=20)
# split test df into vecs and encoded scores
testVecs = testDF.copy()
testVecs = testVecs.drop('score', axis=1)
testScores = to_categorical(testDF['score'])

## Training ##
# Model for binary categorization from word vector #
vec_size=300

model = Sequential([
    Dense(300, input_shape=(vec_size,)),
    Activation('relu'),
    Dense(2),
    Activation('softmax')
])

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print(f"\n{'-'*40}\n{trainVecs}")

model.fit(trainVecs, trainScores, epochs=10)


print(model.metrics_names)
print(model.evaluate(testVecs, testScores))






















pass
