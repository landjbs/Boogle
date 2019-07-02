loadLambda = lambda loadtime: loadTime

def calc_base_score(loadTime):
    """
    Establishes base score for page during crawl to avoid
    storing page attributes that won't change and aren't
    necessary for searching
    """
    base_score = loadLambda(loadTime)
    return base_score
