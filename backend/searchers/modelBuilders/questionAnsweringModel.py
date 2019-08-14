import numpy as np
import pandas as pd
import tensorflow as tf
from os import listdir
from functools import reduce
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, GRU, Bidirectional, ConvLSTM2D, Masking, TimeDistributed, CuDNNGRU
from keras.utils import plot_model


def train_answering_lstm(folderPath, outPath=None):
    """
    Trains bidirectional LSTM model on dataframe of feature arrays and
    target vectors in dataframe pickled at filePath.
        -folderPath:    Path to folder under which the dataframe is tableted
        -outPath:       Path to which to save the trained model
    """

    # build dataframe form tablets under folderPath
    tabletList = []
    for i, file in enumerate(listdir(folderPath)):
        if file.endswith('.sav') and i < 1000:
            tablet = pd.read_pickle(f'{folderPath}/{file}', compression='gzip')
            tabletList.append(tablet)

    dataframe = pd.concat(tabletList)

    features, targets = dataframe['features'], dataframe['targets']

    del dataframe

    # reshape the feature and target arrays
    featureArray = np.array([feature for feature in features])
    targetArray = np.array([np.array(target) for target in targets])

    del features
    del targets

    # # Display
    # plt.plot(np.sum(targetArray, axis=0))
    # plt.xlabel('Token Num')
    # plt.ylabel('Number of Times in Span')
    # plt.show()

    print(featureArray)

    maskArray = np.zeros(featureArray.shape[2])

    import keras
    from keras_self_attention import SeqSelfAttention

    inputs = keras.layers.Input(shape=[404, 768], name='encodings')
    lstm_out = keras.layers.Bidirectional(keras.layers.LSTM(units=80, return_sequences=True))(inputs)
    # attn = SeqSelfAttention(attention_activation='relu')(lstm_out)
    output = keras.layers.Dense(units=1, activation='softmax')(attn)
    output = keras.layers.Reshape([404])(output)

    model = keras.models.Model(inputs=inputs, outputs=output)
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    # # model architecture
    # model = Sequential()
    # model.add(Masking(mask_value=maskArray))
    # model.add(Bidirectional(LSTM(200), input_shape=(featureArray.shape[1],
    #                                             featureArray.shape[2])))
    # model.add(Dense(targetArray.shape[1]))
    # model.add(Activation('softmax'))
    #
    # # model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    # model.compile(loss='categorical_crossentropy',
    #                 optimizer='adam',
    #                 metrics=['accuracy'])

    # model training
    model.fit(featureArray, targetArray, batch_size=20,
                epochs=50, validation_split=0.1)

    if outPath:
        model.save(outPath)

    print(model.summary())

    return model
