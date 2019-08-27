import json
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
    def __init__(self, name, questionLength, contextLength):
        assert isinstance(name, str), f'name expected type string, but found type {type(name)}'
        assert isinstance(questionLength, int), f'questionLength expected type int, but found type {type(name)}'
        assert isinstance(contextLength, int), f'contextLength expected type int, but found type {type(name)}'
        self.name = name
        self.questionLength = questionLength
        self.contextLength = contextLength
        self.wordIdx = None
        self.vocabSize = 0

    def __repr__(self):
        return (f"<LanguageObject NAME={self.name} "
                f"QUESTION_LENGTH={self.questionLength} "
                f"CONTEXT_LENGTH={self.contextLength} "
                f"VOCAB_SIZE={self.vocabSize}>")

    def initialize_from_squad(self, squadPath):
        """ Reads squad file to initialize Language attributes """
        tokenSet = set()

        def clean_tokenize_and_add(rawString):
            """ Cleans and tokenizess raw string and adds tokens to tokenSet """
            cleanString = rawString.strip().lower()
            textTokens = word_tokenize(cleanString)
            for token in textTokens:
                tokenSet.add(token)
            return True

        with open(squadPath, 'r') as squadFile:
            for category in tqdm(json.load(squadFile)['data']):
                clean_tokenize_and_add(category['title'])
                for paragraph in category['paragraphs']:
                    clean_tokenize_and_add(paragraph['context'])
                    for question in paragraph['qas']:
                        clean_tokenize_and_add(question['question'])

        wordIdx = {word : i for i, word in enumerate(tokenSet)}
        vocabSize = len(wordIdx)
        assert (vocabSize  == (max(wordIdx.values()) + 1)), f'Indexing error'
        self.vocabSize = vocabSize
        self.wordIdx = wordIdx
        return True

    def reverse_idx(self):
        self.reverseIdx = {i : word for word, i  in self.wordIdx.items()}


english = LanguageConfig('bert', 10, 100)
print(english)
english.initialize_from_squad(SQUAD_PATH)
print(english)
