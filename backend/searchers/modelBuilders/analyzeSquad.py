import json
import numpy as np
from tqdm import tqdm, trange
from nltk.tokenize import word_tokenize

class TrainingPadding(object):
    """ Pads training data to be a multiple of batch size. """


class TrainingInstance(object):
    """ Instance of question and answer span upon which to train """
    def __init__(self, qId, cId, answerable):
        """
        qId:            Unique string id of question
        cId:            Unique int id of context paragraph
        answerable:     Boolean; whether the question is answerable

        """

SQUAD_PATH = '../../data/inData/squad/train-v2.0.json'

class LanguageConfig(object):
    """
    Class storing information about the language such as wordId index,
    vocabulary size, and maximum sequence lengths.
    """
    def __init__(self, name, questionLength, contextLength, tokenizer,
                observationNum=0):
        # assertions
        assert (isinstance(name, str),
                f'name expected type string, but found type {type(name)}')
        assert (isinstance(questionLength, int),
                ('questionLength expected type int'
                f'but found type {type(name)}'))
        assert (isinstance(contextLength, int),
                f'contextLength expected type int, but found type {type(name)}')
        assert callable(tokenizer), f'tokenize must be callable'
        assert (isinstance(observationNum, int),
                ('observationNum expected type int'
                f'but found type {type(observationNum)}'))
        # initializations
        self.name = name
        self.questionLength = questionLength
        self.contextLength = contextLength
        self.tokenizer = tokenizer
        self.wordIdx = None
        self.vocabSize =
        self.observationNum = observationNum

    def __repr__(self):
        return (f"<LanguageObject NAME={self.name} "
                f"QUESTION_LENGTH={self.questionLength} "
                f"CONTEXT_LENGTH={self.contextLength} "
                f"VOCAB_SIZE={self.vocabSize} "
                f"OBSERVATION_NUM={self.observationNum}>")

    def initialize_from_squad(self, squadPath):
        """ Reads squad file to initialize Language attributes """
        tokenSet = set()
        observationNum = 0

        def clean_tokenize_and_add(rawString):
            """ Cleans and tokenizess raw string and adds tokens to tokenSet """
            cleanString = rawString.strip().lower()
            textTokens = self.tokenizer(cleanString)
            for token in textTokens:
                tokenSet.add(token)

        with open(squadPath, 'r') as squadFile:
            for category in tqdm(json.load(squadFile)['data']):
                clean_tokenize_and_add(category['title'])
                for paragraph in category['paragraphs']:
                    clean_tokenize_and_add(paragraph['context'])
                    for question in paragraph['qas']:
                        clean_tokenize_and_add(question['question'])
                        observationNum += 1

        wordIdx = {word : i for i, word in enumerate(tokenSet)}
        self.vocabSize = len(wordIdx)
        self.wordIdx = wordIdx
        self.observationNum = observationNum
        return True

    def reverse_idx(self):
        self.reverseIdx = {i : word for word, i  in self.wordIdx.items()}
        return True

    def token_to_id(self, token):
        """ Converts token to token id using wordIdx dict """
        return self.wordIdx[token]

    def token_list_to_id_list(self, tokenIds):
        """ Uses token_to_id dict to map a token list into an id list """
        return list(map(self.token_to_id()), tokenIds)

    def text_to_id_list(self, rawText):
        """ Uses tokenizer to tokenize raw text and convert to id list """
        textTokens = self.tokenize(rawText.strip().lower())
        return token_list_to_id_list(textTokens)

e = LanguageConfig('bert', 10, 'hi', word_tokenize)
e.initialize_from_squad(SQUAD_PATH)

text = 'the man runs'
print(e.text_to_id_list(text))



# def squad_to_training_data(squadPath, config):
#     """
#     Converts data from squadPath to...
#     A 3rd rank feature tensor of shape:
#     (observation_num, (question_length + context_length), 3) where 3 is the
#     number of features for each token in an observation (input_ids, input_masks,
#     segment_ids) and input_ids are scalar token ids for each token, input_masks
#     are binary indicators of whether a token should be analyzed, and
#     segment_ids are binary indicators of whether a token belongs to the question
#     or context in packed sequence.
#     And to a 3rd rank target tensor of shape:
#     (observation_num, context_length, 2) where 2 is the number of target arrays.
#     Both target arrays are binary one-hot vectors encoding start location and
#     end location of answer span respectively.
#     """
#     assert (isinstance(config, LanguageConfig),
#             f'config expected type LanguageConfig but got type {type(config)}')
#
#     # cache config info
#     questionLength = config.questionLength
#     contextLength = config.contextLength
#     observationNum = config.observationNum
#     packedLength = questionLength + contextLength
#     # instantiate zero arrays for features and targets
#     featureArray = np.zeros(shape=(observationNum, packedLength, 3))
#     targetArray = np.zeros(shape=(observationNum, contextLength, 2))
#     # iterate over squad file, filling feature and target arrays
#     curObservation = 0
#     with open(squadPath, 'r') as squadFile:
#         for category in tqdm(json.load(squadFile)['data']):
#             for paragraph in category['paragraphs']:
#                 paragraphText = paragraph['context']
#                 paragraphIds = config.token_list_to_id_list(paragraphTokens)
#                 featureArray
