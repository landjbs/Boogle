"""
Class defining posting lists, related tokens, and metrics for tokens in thicctable
"""

### LAMBDAS CALLED BY POSTING FUNCTIONS ###
# check_url examines the url from a page obj (second elt of page tuple)
check_url = lambda pageTuple : (pageTuple[1].url != url)
# get_score gets the score from a page tuple (the first elt)
get_score = lambda pageTuple : pageTuple[0]
# get_pageObj gets the pageObj from a pageTuple (the second elt)
get_pageObj = lambda pageTuple : pageTuple[1]
# get pageObj from pageTuple and apply .describe method
display_pageTuple = lambda pageTuple : pageTuple[1].display(tokenList)

class Posting():

    def __init__(self, relatedTokens=[]):
        """ Postings are initialized as empty posting and related lists """
        self.postingList = []
        self.relatedTokens = relatedTokens

    ### FUNCTIONS FOR MODIFYING POSTING LIST ###
    def add_to_postingList(self, pageTuple):
        """ Adds pageTuple to the end of postingList """
        self.postingList.append(pageTuple)
        return True

    def sort_postingList(self):
        """ Sorts posting list of pageTuples in descending order """
        self.postingList = self.postingList.sort(reverse=True, key=get_score)
        return True

    def clear_postingList(self):
        """ Clears posting list to empty """
        self.postingList = []
        return True

    def clip_postingList(self, n):
        """ Clips posting list to n pageTuples """
        self.postingList = self.postingList[:n]
        return True

    def remove_from_postingList(self, url):
        """ Removes pageTuple of pageObj with url from posting list """
        self.postingList = list(filter(check_url, self.postingList))
        return True

    def len_posting(self):
        """ Returns length of postingList """
        return len(self.postingList)

    def is_empty(self):
        """ Checks if the postingList is empty """
        return (self.postingList == [])

    def search_display_topPostings(self, tokenList, n):
        """
        Returns display tuple from top n pages from (sorted) key with
        window text according to token list
        """
        return list(map(display_pageTuple, self.postingList[:n]))

    def search_pageObj_topPostings(self, key, n):
        """
        Returns list of page objects in key, discarding scores.
        Useful if pages need to be reranked (eg. and_search).
        """
        return list(map(get_pageObj, self.postingList[:n]))

    def search_full_topPostings(self, key, n):
        """ Returns the top n pageTuples of the list mapped by key in invertedIndex """
        return self.postingList[:n]

    ### FUNCTIONS FOR MODIFYING RELATED TOKENS LIST ###
    def add_to_relatedTokens(self, token, index=None):
        """
        Adds token to index of relatedTokens list. Token is added to the end
        if no index is given NOT COMPLETE
        """
        # if index:
        #     self.relatedTokens =
        self.relatedTokens.append(token)

    def remove_from_relatedTokens(self, token):
        """ Removes token from relatedTokens, if it's there """
        try:
            self.relatedTokens.remove(token)
            return True
        except Exception as e:
            print(f'relatedToken Removal Error: {e}')
            return False

    def clip_relatedTokens(self, n):
        """ Clips relatedTokens list to lenght n """
        self.relatedTokens = self.relatedTokens[:n]
        return True

    def clear_relatedTokens(self):
        """ Clears all tokens from relatedTokens list """
        self.relatedTokens = None
        return True
