#Import all the dependencies
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
nltk.download('punkt')

data = ["peach pie", "berry cake", "small man"]

# list mapping list of document tokens to unique integer tag
tagged_data = [TaggedDocument(words=nltk.tokenize.word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

# set hyperparams for model training
max_epochs = 100
vec_size = 20
alpha = 0.025

# initialize model
model = Doc2Vec(size=vec_size,
                alpha=alpha,
                min_alpha=0.00025,
                min_count=1,
                dm =1)

#
model.build_vocab(tagged_data)

print(model)
#
# for epoch in range(max_epochs):
#     print(f'\tIteration {epoch}', end="\r")
#     model.train(tagged_data,
#                 total_examples=model.corpus_count,
#                 epochs=model.iter)
#     # decrease the learning rate
#     model.alpha -= 0.0002
#     # fix the learning rate, no decay
#     model.min_alpha = model.alpha
#
# model.save("d2v.model")
# print("Model Saved")
#
# from gensim.models.doc2vec import Doc2Vec
#
# model= Doc2Vec.load("d2v.model")
# #to find the vector of a document which is not in training data
# test_data = nltk.tokenize.word_tokenize("apple pie".lower())
# v1 = model.infer_vector(test_data)
# # print("V1_infer", v1)
#
# # to find most similar doc using tags
# similar_doc = model.docvecs.most_similar('0')
# print(similar_doc)
#
#
# # to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
# # print(model.docvecs['1'])
