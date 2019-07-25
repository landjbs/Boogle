def score_simple_intersection(pageObj, tokenWeights):
    """
    Scores page by load time and score of multiple tokens
    """
    tokenScore = pageObj.baseScore
    pageTokens = pageObj.knowledgeTokens

    for curTokens, curWeight in tokenWeights.items():
        if curToken in pageTokens:
            tokenScore += curWeight * knowledgeTokens[token]
        else:
            tokenScore -= curWeight

    load
