"""
Defines the Page() class, which is used to concisely store information about
webpages in an accessible way.
"""

from searchers.displayWindow import bold_and_window

class Page():
    """
    Stores attribues of a webpage. Thicctable buckets are lists of Page objects
    """
    def __init__(self, url, title, knowledgeTokens, linkList, loadTime, loadDate, windowText):
        """ Initialize page object with page features """
        self.url = url
        self.title = title
        self.knowledgeTokens = knowledgeTokens
        self.linkList = linkList
        self.loadTime = loadTime
        self.loadDate = loadDate
        self.windowText = windowText


    def display(self, tokenList):
        """
        Returns the parts of the page that would be displayed as search results
        """
        return (self.url, self.title, bold_and_window(tokenList, self.windowText))
