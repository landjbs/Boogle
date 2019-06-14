# scoring lambdas that map page-related scalars onto functions
loadLambda = lambda loadTime : loadTime**(2)

# import matplotlib.pyplot as plt
# plt.plot([loadLambda(i) for i in range(1,10)])
# plt.show()


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

    totalScore = tokenScore
    return totalScore
