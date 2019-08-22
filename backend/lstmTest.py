from os import listdir
import numpy as np
import pandas as pd
import keras

folderPath = 'data/outData/searchAnalysis/squadDataFrames'
OUT_PATH = 'data/outData/searchAnalysis/quetsionAnsweringModels.sav'

# build dataframe form tablets under folderPath
tabletList = []
for i, file in enumerate(listdir(folderPath)):
    if file.endswith('.sav') and i < 100:
        tablet = pd.read_pickle(f'{folderPath}/{file}', compression='gzip')
        tabletList.append(tablet)
        print(f'Tableting: {i}')

dataframe = pd.concat(tabletList)

features, targets = dataframe['features'], dataframe['targets']

del dataframe

# reshape the feature and target arrays
featureArray = np.array([feature for feature in features])
targetArray = np.array([np.array(target) for target in targets])

del features
del targets

inputs = keras.layers.Input(shape=(404, 768), name='embeddings')
lstm = keras.layers.Bidirectional(keras.layers.LSTM(units=768, return_sequences=True))(inputs)
dense = keras.layers.Dense(units=100, activation='relu')(lstm)
flat = keras.layers.Flatten()(dense)
outputs = keras.layers.Dense(units=404, activation='softmax')(flat)

model = keras.models.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print(model.summary())

trainHistory = model.fit(featureArray, targetArray, validation_split=0.1, epochs=80, batch_size=10)

model.save(OUT_PATH)
