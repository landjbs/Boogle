# scoring lambdas that map page-related scalars onto functions
# function to penalize long load times
loadLambda = lambda loadTime : loadTime
# function to normalize aggregateScore of page to avoid huge outliers NO IMP YET!
normalizationLambda = lambda aggregateScore : aggregateScore

## Load ML Models ##
# from models.binning.docVecs import docVec_to_dict
# from keras.models import load_model
# import pandas as pd
# binaryModel = load_model('data/outData/binning/binaryModel.sav')
####################


def score_single(pageObj, token):
    """
    Ranks pageObj based on attributes
    """

    # pull out the token-specific score assigned by knowledgeFinder
    tokenScore = pageObj.knowledgeTokens[token]
    # score page based on loading speed
    loadPenalty = loadLambda(pageObj.loadTime)

    ### Test ranker to score news higher STILL UNDER CONSTRUCTION ###
    # dfVec = pd.DataFrame([docVec_to_dict(pageObj.pageVec)])
    # print(dfVec)
    # newsScore = (binaryModel.predict(dfVec))[1]
    # newsBooster = 4 if (newsScore > 0.4) else 0
    #################################################################

    aggregateScore = tokenScore - loadPenalty
    normalizedScore = normalizationLambda(aggregateScore)
    return normalizedScore


def score_intersection(pageObj, tokenList):
    """
    Scores page by load time and score list of multiple tokens
    """
    tokenScore = 0
    knowledgeTokens = pageObj.knowledgeTokens

    # aggregate score for each token in token list
    # (pages with absent tokens aren't punished currently)
    for token in tokenList:
        try:
            tokenScore += knowledgeTokens[token]
        except:
            pass

    loadPenalty = loadLambda(pageObj.loadTime)

    aggregateScore = tokenScore - loadPenalty
    normalizedScore = normalizationLambda(aggregateScore)

    print(f"{pageObj.url}\n\t{normalizedScore}")

    return normalizedScore
