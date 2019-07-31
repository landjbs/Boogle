"""
Object to store all data about results passed from app.py to result.html
"""

class ResultObject():

    def __init__(self, rawSearch, searchLen, pagesReturned, correction,
                invertedResult, questionAnswer, searchTime, user):
        """
            -rawSearch:         The raw string of the search text
            -searchLen:         The amount of time the search took to complete
            -pagesReturned:     The number of pages returned for the search
            -correction:        The string of the corrected raw search; None if no change
            -invertedResult:    The page tuple of an inverted result if one is to be shown; None otherwise
            -questionAnswer:    The answer to a search question if one is to be shown; None otherwise
            -searchTime:        The time at which the search was undertaken
            -user:              The user who initiated the search
        """
        self.rawSearch          =   rawSearch
        self.searchLen          =   searchLen
        self.pagesReturned      =   pagesReturned
        self.correction         =   correction
        self.invertedResult     =   invertedResult
        self.questionAnswer     =   questionAnswer
        self.searchtime         =   searchTime
        self.user               =   user
