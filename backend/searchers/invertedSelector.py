"""
Decides which (of any) page to display as an inverted result
"""

def selected_inverted(correctedSearch, resultList, n):
    """
    Analyzes top n pages from result list to find eith 1 or 0 selections for
    an inverted display.
    Args:
        -correctedSearch:           The string of the corrected search
        -resultList:                List of Page() objects found by querying
                                        database for correctedSearch
        -n:                         Number of pages from the top of resultList
                                        to analyze as inverted candidates
    Returns:
        -invertedResult:            Page() object of the inverted result if
                                        there is one, otherwise None
        -resultList:                Same as resultList passed as arg, with
                                        Page() object of invertedResult removed
                                        if there is one
        As tuple of form (invertedResult, resultList)
    """
    for i, page in enumerate(resultList[:n]):
        if (correctedSearch) == (page.title.lower().strip()):
            invertedResult =  resultList.pop(i)
            return (invertedResult, resultList)
    return (None, resultList)
