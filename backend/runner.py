from searchers.modelBuilders.questionAnsweringModel import train_answering_lstm

train_answering_lstm('data/outData/searchAnalysis/squadDataFrames',
                    outPath='answerModel.h5')
