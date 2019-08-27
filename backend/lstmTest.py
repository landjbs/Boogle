from searchers.modelBuilders.analyzeSquad import *

SQUAD_PATH = '../../data/inData/squad/train-v2.0.json'


squadConfig = LanguageConfig(name='squadConfig', questionLength=15, contextLength=500, tokenizer=word_tokenize)
squadConfig.initialize_from_squad(SQUAD_PATH)
squad_to_training_data(SQUAD_PATH, squadConfig, outFolder=)
