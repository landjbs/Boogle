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
        self.url                    =   pageDict['url']
        self.title                  =   pageDict['title']
        self.knowledgeTokens        =   pageDict['knowledgeTokens']
        self.pageVec                =   pageDict['pageVec']
        self.linkList               =   pageDict['linkList']
        self.loadDate               =   pageDict['loadDate']
        self.baseScore              =   pageDict['baseScore']
        self.windowText             =   pageDict['windowText']

    def display(self, tokenList):
        """
        Returns the parts of the page to be displayed as search results
        """
        return (self.url, self.title, bold_and_window(tokenList, self.windowText))

    def display_inverted(self, tokenList):
        """
        Returns the parts of the page that would be displayed an inverted result
        """
        return (self.url, self.title, f"{(self.windowText)[:15000]}...")
