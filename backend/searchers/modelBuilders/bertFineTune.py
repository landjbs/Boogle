import keras
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tqdm import tqdm, trange

class BertLayer(tf.keras.layers.Layer):
    def __init__(
        self,
        n_fine_tune_layers=10,
        pooling="first",
        bert_path="https://tfhub.dev/google/bert_uncased_L-12_H-768_A-12/1",
        **kwargs,
    ):
        self.n_fine_tune_layers = n_fine_tune_layers
        self.trainable = True
        self.output_size = 768
        self.pooling = pooling
        self.bert_path = bert_path
        if self.pooling not in ["first", "mean"]:
            raise NameError(
                f"Undefined pooling type (must be either first or mean, but is {self.pooling}"
            )

        super(BertLayer, self).__init__(**kwargs)


    def build(self, input_shape):
        print('building')
        self.bert = hub.Module(
            self.bert_path, trainable=self.trainable, name=f"{self.name}_module"
        )

        # Remove unused layers
        trainable_vars = self.bert.variables
        if self.pooling == "first":
            trainable_vars = [var for var in tqdm(trainable_vars) if not "/cls/" in var.name]
            trainable_layers = ["pooler/dense"]

        elif self.pooling == "mean":
            trainable_vars = [
                var
                for var in trainable_vars
                if not "/cls/" in var.name and not "/pooler/" in var.name
            ]
            trainable_layers = []
        else:
            raise NameError(
                f"Undefined pooling type (must be either first or mean, but is {self.pooling}"
            )

        # Select how many layers to fine tune
        for i in range(self.n_fine_tune_layers):
            trainable_layers.append(f"encoder/layer_{str(11 - i)}")

        # Update trainable vars to contain only the specified layers
        trainable_vars = [
            var
            for var in trainable_vars
            if any([l in var.name for l in trainable_layers])
        ]

        # Add to trainable weights
        for var in trainable_vars:
            self._trainable_weights.append(var)

        for var in self.bert.variables:
            if var not in self._trainable_weights:
                self._non_trainable_weights.append(var)

        super(BertLayer, self).build(input_shape)


    def call(self, inputs):
        inputs = [K.cast(x, dtype="int32") for x in inputs]
        input_ids, input_mask, segment_ids = inputs
        bert_inputs = dict(
            input_ids=input_ids, input_mask=input_mask, segment_ids=segment_ids
        )
        if self.pooling == "first":
            pooled = self.bert(inputs=bert_inputs, signature="tokens", as_dict=True)[
                "pooled_output"
            ]
        elif self.pooling == "mean":
            result = self.bert(inputs=bert_inputs, signature="tokens", as_dict=True)[
                "sequence_output"
            ]

            mul_mask = lambda x, m: x * tf.expand_dims(m, axis=-1)
            masked_reduce_mean = lambda x, m: tf.reduce_sum(mul_mask(x, m), axis=1) / (
                    tf.reduce_sum(m, axis=1, keepdims=True) + 1e-10)
            input_mask = tf.cast(input_mask, tf.float32)
            pooled = masked_reduce_mean(result, input_mask)
        else:
            raise NameError(f"Undefined pooling type (must be either first or mean, but is {self.pooling}")

        return pooled

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_size)


def build_model(max_seq_length):
    print('1')
    in_id = tf.keras.layers.Input(shape=(max_seq_length,), name="input_ids")
    in_mask = tf.keras.layers.Input(shape=(max_seq_length,), name="input_masks")
    in_segment = tf.keras.layers.Input(shape=(max_seq_length,), name="segment_ids")
    bert_inputs = [in_id, in_mask, in_segment]
    print('2')
    bert_output = BertLayer(n_fine_tune_layers=3, pooling="first")(bert_inputs)
    dense = tf.keras.layers.Dense(256, activation='relu')(bert_output)
    pred = tf.keras.layers.Dense(1, activation='sigmoid')(dense)
    print('3')
    model = tf.keras.models.Model(inputs=bert_inputs, outputs=pred)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print('4')
    model.summary()
    return model


def initialize_vars(sess):
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())
    sess.run(tf.tables_initializer())
    K.set_session(sess)

print('defs')

MAX_LEN = 10
text = 'hi how are you today'
idxDict = {word : (i + 1) for i, word in enumerate(set(text.split()))}
textIds = [idxDict[word] for word in text.split()] + [0 for _ in range(MAX_LEN - len(text.split()))]
textMasks = [1 for  _ in range(len(textIds))] + [0 for _ in range(MAX_LEN - len(textIds))]
textSegments = [0 for _ in range(MAX_LEN)]
trainSegments = [0, 1] + [0 for _ in range(MAX_LEN - 2)]

model = build_model(MAX_LEN)
print(model.summary())
initialize_vars(sess)
print('init')
model.fit(
    [textIds, textMasks, textSegments],
    train_labels,
    epochs=1,
    batch_size=1
)


# def build_data(sampleNum=10000):
#     features = []
#     targets = []
#     for _ in range(sampleNum):
#         numVec = np.random.randint(0,100, size=10)
#         targetVec = np.zeros(shape=(10))
#         try:
#             targetVec[list(numVec).index(5)] = 1
#         except ValueError:
#             pass
#         features.append(numVec)
#         targets.append(targetVec)
#     return np.array(features), np.array(targets)
#
# features, targets = build_data()
# print(features.shape)
# print(targets.shape)
#
# def build_model():
#     """ Builds QA model to optimize start and end vectors """
#     # takes block of questsion and answer
#     inputs = keras.layers.Input(shape=(404,), name='block_embeddings')
#     # flatInputs = keras.layers.Flatten(name='flattened_embeddings')(inputs)
#     # start vector to be optimized
#     startVec = keras.layers.Dense(units=1,
#                                     input_shape=(404, 768),
#                                     activation='softmax',
#                                     name='start_vector')(inputs)
#     # end vector to be optimized
#     endVec = keras.layers.Dense(units=768, activation='softmax', name='end_vector')
#     # dot product of training start vector and flattened inputs
#     startDot = keras.layers.Dot(axes=0)([inputs, startVec])
#
#     # dot product of training end vector and flattened inputs
#     startScalar = keras.layers.Lambda(lambda startDot : startDot[0])(startDot)
#     endScalar = keras.layers.Lambda
#
#     # startMul = keras.layers.Multiply()([inputs, startVec])
#     # activation = keras.layers.Dense(units=100, activation='sigmoid')(startMul)
#     model = keras.models.Model(inputs=inputs, outputs=startScalar)
#     model.compile(optimizer='adam', loss='categorical_crossentropy')
#     print(model.summary())
#
# build_model()
#
# import tensorflow as tf
