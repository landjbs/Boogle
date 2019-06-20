"""
Document vectorization is a method of mapping a text document into a vector
of n values. While the length of this vector is determined by the programmer,
the relative values of different documents are assigned by a machine learning
algorithm trained for word and phrase prediction on BOW and PV-DM constructed
from a training corpus. The approach is detailed in:
https://cs.stanford.edu/~quocle/paragraph_vector.pdf.
docVecs contains functions for training and applying such a model to vectorize
pageText extracted from urls during scraping. The spatial relationship between
paragraph vectors is examined in models/binning/clustering, which attempts
to find clusters within pages that have the knowledge tokens. By clustering
the contents of a val list in the thicctable key-val store, I hope to allow
for more precise, intent-specific search results than those obtained via a
simple reverse index.
"""


from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.parsing.preprocessing import strip_numeric, remove_stopwords
import nltk
import smart_open # for opening documents
from warnings import simplefilter
import multiprocessing # for faster model training
import matplotlib.pyplot as plt
from os import listdir

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
    tokens = nltk.tokenize.word_tokenize(cleanStr)
    return tokens


def train_d2v(folderPath, outPath='d2vModel.sav', max_epochs=100, vec_size=300, alpha=0.025):
    """
    Trains doc vec model contents of folderPath of raw docs and saves model to outPath
    """
    print(f"\n{'-'*40}\nTraining '{outPath}' model:")

    def tag_doc(file, index):
        """
        Helper to tag documents with unique int (index of doc in folder)
        """
        with open(f"{folderPath}/{file}") as FileObj:
            text = FileObj.read()
            tokenized_text = vector_tokenize(text)
        print(f"\tAnalyzing: {index}", end="\r")
        return TaggedDocument(words=tokenized_text, tags=[str(index)])

    # create list of tagged texts from files in folderPath
    tagged_data = [tag_doc(file, i) for i, file in enumerate(listdir(folderPath))]

    # list mapping list of document tokens to unique integer tag
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

    # save model to outPath
    model.save(outPath)
    print(f"Model saved to '{outPath}'.\n{'-'*40}")


def load_model(path):
    """ Loads gensim model from path to avoid re-importing Doc2Vec """
    return Doc2Vec.load(path)


def vectorize_document(doc, model):
    """ Vectorizes document with d2v model stored at modelPath """
    # return document vector for tokenized input doc
    return model.infer_vector(vector_tokenize(doc))


def docVec_to_dict(docVec):
    """ Converts docVec to dict for easy df insertion """
    return {i:scalar for i, scalar in enumerate(docVec)}


def visualize_vecDict(vecDict):
    """ Plots dict mapping titles to docVecs to determine differences """
    for url in vecDict:
        plt.plot(vecDict[url])
    plt.legend([key for key in vecDict])
    plt.title(f'Vectors for {len(vecDict)} Documents')
    plt.xlabel('Vector Dimensions')
    plt.ylabel('Document Value')
    plt.show()


# Train imdb model #
# textList = []
# for doc in os.listdir('data/inData/imdbData.in/train/neg/'):
#     with open('data/inData/imdbData.in/train/neg/' + doc, 'r') as file:
#         text = "".join([line for line in file])
#         textList.append(text)
#
# for doc in os.listdir('data/inData/imdbData.in/train/pos'):
#     with open('aclImdb/train/pos/' + doc, 'r') as file:
#         text = "".join([line for line in file])
#         textList.append(text)
#
#
# train_d2v(textList)












pass
