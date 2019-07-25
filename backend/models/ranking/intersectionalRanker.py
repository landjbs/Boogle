def score_simple_intersection(pageObj, tokenWeights):
    """
    Scores page by load time and score of multiple tokens
    """
    baseScore = pageObj.baseScore
    pageTokens = pageObj.knowledgeTokens
    knowledgeScore = 0

    for curTokens, curWeight in tokenWeights.items():
        if curToken in pageTokens:
            knowledgeScore += curWeight * knowledgeTokens[token]
        else:
            knowledgeScore -= curWeight
            
    aggregateScore = baseScore + knowledgeScore

    return aggregateScore
