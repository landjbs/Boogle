def keywordRank():
    """
    Rank page by weighted frequency at which the knowledge token is used,
    normalized by the length of the page and the frequency of the
    knowledge token in normal English.
    Weights in weighted frequency are based on where in the page the token
    is used.
    """
    
