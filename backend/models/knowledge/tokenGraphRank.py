"""
A tokenized page can be viewed as a force-directed graph in which the vertices
are words, each token's base score on the page is the vertex weighting,
the edges are the relationships between the words, and the strength of the
relationship between tokens is the edge ranking. This structure lends itself
to graph-optimization techniques which can be used to bolster the rankings
of those tokens that are strongly related to 'important' tokens on the page,
even if the token does not have a particularly high base ranking.
This method builds off of the concept of token relationships as defined in
knowledgeRelations and shadow tokens as defined in shadowTokenization, as well
as the graph optimization method, PageRank.
"""

def rank_token_graph(knowledgeTokens, relationshipDict, iterations):
    """
    Runs weighted modification of the PageRank algorithim over
    knowledgeTokens (vertexes) and relationshipDict (edges) for {iterations]
    to return knowledgeTokens with modified scores. Tokens which are pointed
    to with a high relationship score from other important tokens will recieve
    a boosted score, those which are less significantly pointed to will recieve
    a diminished score.
    Args:
        knowledgeTokens:        Dict of knowledgeTokens (generally post-shadow)
        relationshipDict:       Dict mapping strength of relationship of all
                                    important token relationships
        iterations:             Number of iterations for which to run the
                                    computation. Since tokens have base scores
                                    before graph ranking begins and since the
                                    graph has few vertices, the computation
                                    should not take many iterations to converge
    """
    # get the sum of the token values in knowledgeTokens
    scoreSum = sum(knowledgeTokens.values())
    # query relationship dict for top related tokens of each knowledgeToken
    tokenRelationships = {token : relationshipDict[token]
                            for token in knowledgeTokens
                            if token in relationshipDict}
    print(scoreSum)
