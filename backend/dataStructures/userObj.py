"""
Class to describe system users for recommendations and location knowledge
"""

class User():
    def __init__(self, ip):
        """ All users must have an ip address """
        # users are stored on an ip level
        self.ip = ip
        # list of rawSearches performed by the user
        self.history = []

    def add_history(searchString):
        self.history.append(searchString)
