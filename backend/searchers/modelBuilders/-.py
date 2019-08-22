import keras
import numpy as np

def build_data(sampleNum=10000):
    

def build_model():
    """ Builds QA model to optimize start and end vectors """
    # takes block of questsion and answer
    inputs = keras.layers.Input(shape=(404,), name='block_embeddings')
    # flatInputs = keras.layers.Flatten(name='flattened_embeddings')(inputs)
    # start vector to be optimized
    startVec = keras.layers.Dense(units=1,
                                    input_shape=(404, 768),
                                    activation='softmax',
                                    name='start_vector')(inputs)
    # end vector to be optimized
    endVec = keras.layers.Dense(units=768, activation='softmax', name='end_vector')
    # dot product of training start vector and flattened inputs
    startDot = keras.layers.Dot(axes=0)([inputs, startVec])

    # dot product of training end vector and flattened inputs
    startScalar = keras.layers.Lambda(lambda startDot : startDot[0])(startDot)
    endScalar = keras.layers.Lambda

    # startMul = keras.layers.Multiply()([inputs, startVec])
    # activation = keras.layers.Dense(units=100, activation='sigmoid')(startMul)
    model = keras.models.Model(inputs=inputs, outputs=startScalar)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    print(model.summary())

build_model()
