"""
"""

from searchers.searchTokenizer import search_tokens
from models.ranking.pageRankers import score_intersection

def search_database(rawSearch, database):
    """
    Parses search and finds results in database.
    Supports multitoken search.
    Doesn't support lexical analysis yet.
    """
    # find all tokens being searched in rawSearch
    searchTokens = get_search_tokens(rawSearch)
    # if only one search token is used, simply search the bucket
    if (len(searchTokens)==1):
        finalResults = database.search_index()
    # query database for n results for each searchToken
    unfilteredResults = [database.search_full(token, n=10000) for token in searchTokens]
    # intialize list to hold newly scored pages
    filteredResults = []
    # iterate over results for first token
    for result in unfilteredResults[0]:
        # score result for all search tokens
        knowledgeTokens = result[2]
        # list to hold scores for all searchTokens in current result
        try:
            scoreList = [knowledgeTokens[token] for token in searchTokens]
            # get score of page based on scoreList and load time
            pageScore = score_intersection(scoreList, result[4])
            # add tuple of page url, title, and score to filteredResults
            filteredResults.append((result[0], result[1], pageScore))
        # skip page if it doesn't have a score for any one of the search tokens
        except:
            pass
    # sort filtered results
    sortedResults
