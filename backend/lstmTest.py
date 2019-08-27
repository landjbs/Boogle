import tensorflow as tf
from tensorflow import keras

from bert import BertModelLayer
from bert import params_from_pretrained_ckpt
from bert import load_stock_weights

from searchers.modelBuilders.analyzeSquad import *
from dataStructures.objectSaver import load, save
# from searchers.modelBuilders.bertFineTune import *
from os import listdir

targets, features  = [np.load(f'data/outData/squadProcessedTraining/{file}')
                        for file in listdir('data/outData/squadProcessedTraining')]
print(features.shape)
textIds = features[0, :, :]
textMasks = features[1, :, :]
textSegments = features[2, :, :]
max_seq_len = 715

assert (textIds.shape == textMasks.shape == textSegments.shape), 'shapes'

train_labels = targets[0, :, :]

model_dir = '/Users/landonsmith/Desktop/shortBert'

bert_params = params_from_pretrained_ckpt(model_dir)
l_bert = BertModelLayer.from_params(bert_params, name="bert")


l_input_ids      = keras.layers.Input(shape=(max_seq_len,), dtype='int32')
# l_token_type_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32')

# using the default token_type/segment id 0
embeddings = l_bert(l_input_ids)
flat = keras.layers.Flatten()(embeddings)
dense = keras.layers.Dense(units=700, activation='softmax')(flat)
model = keras.Model(inputs=l_input_ids, outputs=dense)
print(model.summary())

model.compile(optimizer='adam', loss='categorical_crossentropy')

model.fit(textIds, train_labels, epochs=3)


# from searchers.modelBuilders.analyzeSquad import *
# from dataStructures.objectSaver import load, save
# from searchers.modelBuilders.bertFineTune import *
# from os import listdir
#
# SQUAD_PATH = 'data/inData/squad/train-v2.0.json'
#
#
# # squadConfig = LanguageConfig(name='squadConfig', questionLength=15, contextLength=700, tokenizer=word_tokenize)
# # squadConfig.initialize_from_squad(SQUAD_PATH)
# # save(squadConfig, 'squadConfig')
# # squadConfig = load('squadConfig')
# # squad_to_training_data(SQUAD_PATH, squadConfig, outFolder='data/outData/squadProcessedTraining')
#
#
# targets, features  = [np.load(f'data/outData/squadProcessedTraining/{file}')
#                         for file in listdir('data/outData/squadProcessedTraining')]
# print(features.shape)
# textIds = features[0, :, :]
# textMasks = features[1, :, :]
# textSegments = features[2, :, :]
# MAX_LEN = 715
#
# assert (textIds.shape == textMasks.shape == textSegments.shape), 'shapes'
#
# train_labels = targets[0, :, :]
#
#
# model = build_model(MAX_LEN)
# print(model.summary())
# initialize_vars(sess)
# model.fit(
#     [textIds, textMasks, textSegments],
#     train_labels,
#     epochs=1,
#     batch_size=1
# )
