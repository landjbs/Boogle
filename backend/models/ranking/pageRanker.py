# scoring lambdas that map page-related scalars onto functions
# function to penalize long load times
loadLambda = lambda loadTime : loadTime**(2)
# function to normalize aggregateScore of page to avoid huge outliers NO IMP YET!
normalizationLambda = lambda aggregateScore : aggregateScore


def score(pageList, token):
    """
    Ranks page based on attributes
    """

    # pull out the token-specific score assigned by knowledgeFinder
    tokenScore = pageList[2][token]
    # score page based on loading speed
    loadPenalty = loadLambda(pageList[4])

    # TO DO: Use ML on docVec to categorize page into topic area
    # Use topic area to score page's freshness (eg. news needs to be fresh)

    aggregateScore = tokenScore - loadPenalty
    normalizedScore = normalizationLambda(aggregateScore)
    return normalizedScore
