"""
Stores inverted index mapping ip addresses to the associated user
"""

class UserDatabase():
    def __init__(self):
        self.userDict = {}

    def add_user(self, ip, userObj):
        self.userDict.update({ip : userObj})

    # def search_user(ip):
    #     self.userDict
