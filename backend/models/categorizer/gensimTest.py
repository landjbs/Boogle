from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
nltk.download('punkt')


data = ["peach pie", "berry cake", "small man"]

def train_d2v(data, path='d2v.model', max_epochs=100, vec_size=20, alpha=0.025):
    """ Trains doc vectorization model on iterable of doc and saves model to path """
    # list mapping list of document tokens to unique integer tag
    tagged_data = [TaggedDocument(words=nltk.tokenize.word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

    # initialize model
    model = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)

    # build vector of all words contained in tagged data
    model.build_vocab(tagged_data)

    # train model for max_epochs
    for epoch in range(max_epochs):
        print(f'\tTraining: {epoch}', end="\r")
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
    print(f"Model saved to {path}.")


def vectorize_document(doc, modelPath="d2v.model"):
    """ Vectorizes document with d2v model stored at modelPath """
    # load saved model
    model= Doc2Vec.load("d2v.model")
    # tokenize input doc
    tokenizedDoc = nltk.tokenize.word_tokenize(doc.lower())
    # create document vector for tokenizedDoc
    docVector = model.infer_vector(tokenizedDoc)

    #
    # # to find most similar doc using tags
    # similar_doc = model.docvecs.most_similar('0')
    # print(similar_doc)
    #
    #
    # # to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
    # # print(model.docvecs['1'])


vectorize_document("hi how are you?")







pass
