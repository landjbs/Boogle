loadLambda = lambda loadTime: loadTime

def calc_base_score(baseAttributes):
    """
    Establishes base score for page during crawl to avoid
    storing page attributes that won't change and aren't
    necessary for searching
    """
    loadTime = baseAttributes['loadTime']
    base_score = loadLambda(loadTime)
    return base_score
