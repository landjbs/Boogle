"""
"""

from searchers.searchTokenizer import search_tokens

def search_database(rawSearch, database):
    """
    Parses search and finds results in database.
    Supports multitoken search.
    Doesn't support lexical analysis yet.
    """
