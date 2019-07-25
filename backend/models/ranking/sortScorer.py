"""
Scores single page at sort time as a function of its baseScore, tokenScores,
and any special intersections with the bucket.
"""


# scoring lambdas that map page-related scalars onto functions
# function to penalize long load times
loadLambda = lambda loadTime : loadTime
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


def score_intersection(pageObj, tokenWeights):
    """
    Scores page by load time and score of multiple tokens
    """
    tokenScore = 0
    knowledgeTokens = pageObj.knowledgeTokens

    # tokenScore is the sum of weighted token scores for each token in the page
    for token in tokenWeights:
        try:
            tokenScore += (tokenWeights[token]) * (knowledgeTokens[token])
        except:
            tokenScore -= 1
    print(f"{pageObj.url}\n\t{tokenWeights}")
    loadPenalty = loadLambda(pageObj.loadTime)

    aggregateScore = tokenScore - loadPenalty
    normalizedScore = normalizationLambda(aggregateScore)
    return normalizedScore
