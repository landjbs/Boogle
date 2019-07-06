"""
Defines the Page() class, which is used to concisely store information about
webpages in an accessible way.
"""

from searchers.displayWindow import bold_and_window

class Page():
    """
    Stores attribues of a webpage. Thicctable buckets are lists of Page objects
    """
    def __init__(self, pageDict):
        """ Initialize page object with pageList of features """
        self.url =              pageDict['url']
        self.title =            pageDict['title']
        self.knowledgeTokens =  pageDict['knowledgeTokens']
        self.pageVec =          pageDict['pageVec']
        self.linkList =         pageDict['linkList']
        self.loadTime =         pageDict['loadTime']
        self.loadDate =         pageDict['loadDate']
        self.imageScore =       pageDict['imageScore']
        self.videoScore =       pageDict['videoScore']
        self.windowText =       pageDict['windowText']

    def display(self, tokenList):
        """
        Returns the parts of the page that would be displayed as search results
        """
        return (self.url, self.title, bold_and_window(tokenList, self.windowText))
