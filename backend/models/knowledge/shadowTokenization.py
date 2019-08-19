"""
I define a 'shadow token' as a knowledgeToken that does not occur on a given
page, but who still has a high ability to describe the contents of the page
as indicated by the tokens and sentiment that are explicityly present on the
page. This module attempts to add relevent shadowTokens to the knowlegeTokens
of a page during preprocessing/crawling.
"""

from collections import Counter

def add_shadow_tokens(knowledgeTokens, relationshipDict):
    """
    Adds shadow tokens to the knowledgeTokens of page
    Args:
        knowledgeTokens:        Dict of knowledgeTokens and scores from
                                    knowledgeFinder processing.
        relationshipDict:       Hashmap from tokens to tokens with high
                                    related-ness and generated in
                                    knowledgeRelations.
    """
    relatedCounts = Counter()
    for knowledgeToken, knowledgeScore in knowledgeTokens.items():
        if knowledgeToken in relationshipDict:
            relatedTokens = corrDict[knowledgeToken]
            for relatedScore, relatedToken in relatedTokens:
                weightedScore = knowledgeScore * relatedScore
                if weightedScore > cutoff:
                    relatedCounts.update({relatedToken : weightedScore})
    knowledgeCounter = Counter(knowledgeTokens)
    knowledgeCounter.update(relatedCounts)
