"""
Object to store all data about results passed from app.py to result.html
"""

class ResultObject():

    def __init__(self, rawSearch, runTime, numResults, correction,
                invertedResult, questionAnswer, resultList, searchTime, user):
        """
        Result objects are initialized with search specific info in searchLexer
            -rawSearch:         The raw string of the search text
            -runTime:           The amount of time the search took to complete
            -numResults:          The number of pages returned for the search
            -correction:        The string of the corrected raw search; None if no change
            -invertedResult:    The page tuple of an inverted result if one is to be shown; None otherwise
            -questionAnswer:    The answer to a search question if one is to be shown; None otherwise
            -resultList:        The list of pageTuples to display as regular results
            -searchTime:        The time at which the search was undertaken
            -user:              The user who initiated the search
        """
        self.rawSearch          =   rawSearch
        self.runTime            =   runTime
        self.numResults         =   numResults
        self.correction         =   correction
        self.invertedResult     =   invertedResult
        self.questionAnswer     =   questionAnswer
        self.resultList         =   resultList
        self.searchTime         =   searchTime
        self.user               =   user
        # searchWords NEEDS REWRITE
        self.searchWords        =   rawSearch.split()

    def log(self):
        """ Logs information about the search to the command line """
        print(f'{self.rawSearch}\n\tTime: {self.searchTime}\n\tUser: {self.user.ip}')
