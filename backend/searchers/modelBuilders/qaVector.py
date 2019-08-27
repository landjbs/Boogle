import keras
import numpy as np

def encode_number(num, maxNum=10):
    numEncoding = np.zeros(shape=maxNum)
    numEncoding[num] = 1
    return numEncoding

def build_data(sampleNum=100000):
    features, targets = [], []
    for i in range(sampleNum):
        numVec = np.random.randint(0, 10, size=10)
        targetVec = np.zeros(shape=(10))
        try:
            targetVec[list(numVec).index(5)] = 1
        except ValueError:
            targetVec[0] = 1
        numArray = [encode_number(num) for num in numVec]
        features.append(numArray)
        targets.append(targetVec)
    return np.array(features), np.array(targets)

features, targets = build_data()
print(features[0])
print(targets[0])


def build_model():
    """ Builds QA model to optimize start and end vectors """
    # takes block of questsion and answer
    inputs = keras.layers.Input(shape=(10,), name='block_embeddings')
    # flatInputs = keras.layers.Flatten(name='flattened_embeddings')(inputs)
    # start vector to be optimized
    startVec = keras.layers.Dense(units=10,
                                    input_shape=(10, ),
                                    activation='sigmoid',
                                    name='start_vector')(inputs)
    # end vector to be optimized
    # endVec = keras.layers.Dense(units=768, activation='softmax', name='end_vector')
    # dot product of training start vector and flattened inputs
    # startDot = keras.layers.Dot(axes=1)([inputs, startVec])
    startDot = keras.layers.Multiply()([inputs, startVec])
    activation = keras.layers.Dense(units=10, activation='softmax')(startDot)

    # # dot product of training end vector and flattened inputs
    # startScalar = keras.layers.Lambda(lambda startDot : startDot[0])(startDot)
    # endScalar = keras.layers.Lambda

    # startMul = keras.layers.Multiply()([inputs, startVec])
    # activation = keras.layers.Dense(units=100, activation='sigmoid')(startMul)
    model = keras.models.Model(inputs=inputs, outputs=activation)
    print(model.summary())
    return model


def build_simple():
    inputs = keras.layers.Input(shape=(10,10), name='block_embeddings')
    dense = keras.layers.Dense(units=100, activation='relu')(inputs)
    flat = keras.layers.Flatten()(dense)
    activation = keras.layers.Dense(units=10, activation='softmax')(flat)
    model = keras.models.Model(inputs=inputs, outputs=activation)
    print(model.summary())
    return model


model = build_simple()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(features, targets, batch_size=10, epochs=10, validation_split=0.1)

import matplotlib.pyplot as plt

testVec, testTarget = build_data(sampleNum=10)

for num, vec in enumerate(testVec):
    predictions = model.predict(np.expand_dims(vec, axis=0))
    maxPred = list(predictions[0]).index(max(predictions[0]))
    empty = np.sum(testTarget[num]) == 0
    print(f'Empty: {empty} | Prediction: {vec[maxPred]}')
