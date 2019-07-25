"""
Scores single page at sort time as a function of its baseScore, tokenScores,
and any special intersections with the bucket.
"""

# function to normalize aggregateScore of page to avoid huge outliers NO IMP YET!
normalizationLambda = lambda aggregateScore : aggregateScore


def sort_score(pageObj, token):
    """
    Ranks pageObj based on attributes
    """
    # pull out the token-specific score assigned by knowledgeFinder
    tokenScore = pageObj.knowledgeTokens[token]
    # pull out the base score of the page
    baseScore = pageObj.baseScore

    aggregateScore = tokenScore - loadPenalty
    normalizedScore = normalizationLambda(aggregateScore)
    return normalizedScore
