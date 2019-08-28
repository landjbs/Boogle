config_file = '/Users/landonsmith/Desktop/shortBert/bert_config.json'
checkpoint_file = '/Users/landonsmith/Desktop/shortBert/bert_model.ckpt'
vocab_file = '/Users/landonsmith/Desktop/shortBert/vocab.txt'

import keras
import numpy as np
from os import listdir
from keras_bert.bert import get_model
from keras_bert.loader import load_trained_model_from_checkpoint


from searchers.modelBuilders.analyzeSquad import *
from dataStructures.objectSaver import load, save
from searchers.modelBuilders.bertFineTune import *
from os import listdir

import searchers.modelBuilders.bertTokenizer as tokenization

tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=True)

MAX_LEN = 512
OUT_LEN = 500
SQUAD_PATH = 'data/inData/squad/train-v2.0.json'

# squadConfig = LanguageConfig(name='squadConfig', questionLength=12, contextLength=500, tokenizer=tokenizer)
# squadConfig.initialize_from_squad(SQUAD_PATH)
# save(squadConfig, 'squadConfig')
# squadConfig = load('squadConfig')
# squad_to_training_data(SQUAD_PATH, squadConfig, outFolder='data/outData/squadProcessedTraining')


model = load_trained_model_from_checkpoint(config_file, checkpoint_file,
                                        training=True, seq_len=MAX_LEN)


targets, features  = [np.load(f'data/outData/squadProcessedTraining/{file}')
                        for file in listdir('data/outData/squadProcessedTraining')]
print(features.shape)
textIds = features[0, :, :]
textMasks = features[1, :, :]
textSegments = features[2, :, :]

assert (textIds.shape == textMasks.shape == textSegments.shape), 'shapes'

train_labels = targets[0, :, :]

# get cls layer from bert model
seq_out = model.layers[-6].output
crazy = keras.layers.Dense(units=OUT_LEN, activation='softmax')(seq_out)
# pool_out = keras.layers.Dense(units=1, activation='sigmoid')(seq_out)
fineModel = keras.models.Model(inputs=model.input, outputs=crazy)
adam = keras.optimizers.Adam(lr=2e-5,decay=0.01)
fineModel.compile(optimizer=adam, loss='categorical_crossentropy')
print(fineModel.summary())


fineModel.fit(
    [textIds, textSegments, textMasks],
    train_labels,
    epochs=1,
    batch_size=1
)




# import tensorflow as tf
# from tensorflow import keras
#
# from bert import BertModelLayer
# from bert import params_from_pretrained_ckpt
# from bert import load_stock_weights
#
# from searchers.modelBuilders.analyzeSquad import *
# from dataStructures.objectSaver import load, save
# # from searchers.modelBuilders.bertFineTune import *
# from os import listdir
#
# targets, features  = [np.load(f'data/outData/squadProcessedTraining/{file}')
#                         for file in listdir('data/outData/squadProcessedTraining')]
# print(features.shape)
# textIds = features[0, :, :]
# textMasks = features[1, :, :]
# textSegments = features[2, :, :]
# max_seq_len = 715
#
# assert (textIds.shape == textMasks.shape == textSegments.shape), 'shapes'
#
# train_labels = targets[0, :, :]
#
# model_dir = '/Users/landonsmith/Desktop/shortBert'
#
# bert_params = params_from_pretrained_ckpt(model_dir)
# l_bert = BertModelLayer.from_params(bert_params, name="bert")
#
#
# l_input_ids      = keras.layers.Input(shape=(max_seq_len,), dtype='int32')
# # l_token_type_ids = keras.layers.Input(shape=(max_seq_len,), dtype='int32')
#
# # using the default token_type/segment id 0
# embeddings = l_bert(l_input_ids)
# flat = keras.layers.Flatten()(embeddings)
# dense = keras.layers.Dense(units=700, activation='softmax')(flat)
# model = keras.Model(inputs=l_input_ids, outputs=dense)
# print(model.summary())
#
# model.compile(optimizer='adam', loss='categorical_crossentropy')
#
# model.fit(textIds, train_labels, epochs=3)
#
#
