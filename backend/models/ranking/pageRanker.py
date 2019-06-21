# scoring lambdas that map page-related scalars onto functions
# function to penalize long load times
loadLambda = lambda loadTime : loadTime**(2)
# function to normalize aggregateScore of page to avoid huge outliers NO IMP YET!
normalizationLambda = lambda aggregateScore : aggregateScore


def score_single(pageObj, token):
    """
    Ranks pageObj based on attributes
    """

    # pull out the token-specific score assigned by knowledgeFinder
    tokenScore = pageObj.knowledgeTokens[token]
    # score page based on loading speed
    loadPenalty = loadLambda(pageObj.loadTime)

    # TO DO: Use ML on docVec to categorize page into topic area
    # Use topic area to score page's freshness (eg. news needs to be fresh)

    aggregateScore = tokenScore - loadPenalty
    normalizedScore = normalizationLambda(aggregateScore)
    return normalizedScore


def score_intersection(scoreList, loadTime):
    """
    Scores page by load time and score list of multiple tokens
    """
    # sum scoreList and normalize by number of search tokens
    tokenScore = sum(scoreList) / len(scoreList)
    # score page based on loading speed
    loadPenalty = loadLambda(loadTime)
    aggregateScore = tokenScore - loadPenalty
    normalizedScore = normalizationLambda(aggregateScore)
    return normalizedScore
