import pandas as pd
import os
import sys
import random
import keras
import json

import numpy as np
import tensorflow as tf


config_file = '/Users/landonsmith/Desktop/shortBert/bert_config.json'
checkpoint_file = '/Users/landonsmith/Desktop/shortBert/bert_model.ckpt'

from keras_bert.bert import get_model
from keras_bert.loader import load_trained_model_from_checkpoint
from keras.optimizers import Adam

model = load_trained_model_from_checkpoint(config_file, checkpoint_file,
                                            training=True, seq_len=10)

print(model.summary(line_length=120))


adam = Adam(lr=2e-5,decay=0.01)
maxlen = 50
print('begin_build')
