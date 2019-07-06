"""
Responsible for fixing broken URL strings and fetching page
contents using urllib.
"""

import urllib.request
import re


class ParseError(Exception):
    """ Exception for errors while parsing a link """
    pass


# matcher for url denoted by https:// or http://
urlString = r'https://\S+|http://\S+'
urlMatcher = re.compile(urlString)


def parsable(url):
    """ Returns true if url follows urlMatcher pattern """
    return True if urlMatcher.fullmatch(url) else False


def fix_url(url, rootURL):
    """ Add proper headings URLs for crawler analysis """
    urlString = str(url)
    if not parsable(urlString):
        if urlString.startswith('http'):
            pass
        elif urlString.startswith("www"):
            urlString = "https://" + urlString
        elif urlString.startswith('/'):
            urlString = rootURL + urlString
        else:
            urlString = "http://www." + urlString
    return urlString


def url_to_pageString(url, timeout=10):
    """
    Cleans and converts string of URL link to string of page contents.
    DOESN'T FIX URLS
    """
    try:
        # get response object of url, failing after timeout seconds
        page = urllib.request.urlopen(url, timeout=timeout)
    except:
        raise ParseError(f"Unable to access '{url}'")
    pageString = page.read()
    page.close()
    return(pageString)


def get_robots(url):
    """
    Fetchs robots.txt file from top level url
    """
    return url_to_pageString(f"{url}/robots.txt")
