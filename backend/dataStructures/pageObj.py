"""
Defines the Page() class, which is used to concisely store information about
webpages in an accessible way.
"""

from searchers.displayWindow import bold_and_window

class Page():
    """
    Stores attribues of a webpage. Thicctable buckets are lists of Page objects
    """
    def __init__(self, pageList):
        """ Initialize page object with pageList of features """
        self.url = pageList[0]
        self.title = pageList[1]
        self.knowledgeTokens = pageList[2]
        self.pageVec = pageList[3]
        self.linkList = pageList[4]
        self.loadTime = pageList[5]
        self.loadDate = pageList[6]
        # self.imageNum = pageList[7]
        self.windowText = pageList[7]

    def display(self, tokenList):
        """
        Returns the parts of the page that would be displayed as search results
        """
        return (self.url, self.title, bold_and_window(tokenList, self.windowText))
