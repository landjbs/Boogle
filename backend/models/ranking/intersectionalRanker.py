from scipy.spatial.distance import euclidean

def score_token_intersection(pageObj, tokenWeights):
    """
    Scores page by baseScore and score of multiple tokens
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
    print(f'baseScore: {baseScore} || knowledgeScore: {knowledgeScore}')
    return aggregateScore

def score_vector_intersection(pageObj, tokenWeights, searchVec):
    """
    Scores page by baseScore, score of multiple tokens, and relationship
    with search vector
    """
    pageVec = pageObj.pageVec

    vecScore = euclidean(searchVec, pageVec)

    tokenAndBaseScore = score_token_intersection(pageObj, tokenWeights)
    print(f'vecScore: {vecScore}')
    aggregateScore = tokenAndBaseScore + vecScore
