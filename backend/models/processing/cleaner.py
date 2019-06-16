"""
Implements functions for cleaning text for both specialized (eg. knowledge
tokenization, doc vec training) and broad (eg. pageString cleaning) purposes.
This search engine is built around the desire to store comprehensive search
results as concisely as possible, a philosophy extends to my text
processing: everything that can be removed without interfering with search
result, should be.
Functions:
    -clean_text(): Primarily used to clean pageStrings before analysis
        -Replace \t, \n, and multiple spaces with a single space
        -Remove non-alpha characters
        -Lowercase all alpha characters
"""

import re

## Matchers ##
# matches things that look like a single html tag
tagMatcher = re.compile(r"<[^\s][^<]*>")
# matches non-alpha, space, or sentence-ending punctuation (dash must be at end)
stripMatcher = re.compile(r"[^a-zA-Z\s\t\n_-]")
# matches any sequence of tabs, newlines, spaces, underscores, and dashes
spaceMatcher = re.compile(r"[\t|\n|\s|-|_]+")
# matches \t \r and \n in titles
slashMatcher = re.compile(r"[.\r|.\n|.\t]")
# matches for special parts of url
urlMatcher = re.compile(r"[https|http|www|com|org|edu]")


## Funcitons ##
def clean_text(rawString):
    """
    Cleans rawString by replacing spaceMatcher and tagMatcher with a single
    space, removing non-alpha chars, and lowercasing alpha chars
    """
    # replace spaceMatcher and tagMatcher with " "
    detaggedString = re.sub(tagMatcher, " ", rawString)
    # replace stripMatcher with ""
    cleanedString = re.sub(stripMatcher, "", detaggedString)
    # replace spaceMatcher with " " and strip surround whitespace
    spacedString = re.sub(spaceMatcher, " ", cleanedString).strip()
    # lowercase the alpha chars that remain
    loweredString = spacedString.lower()
    return loweredString


def clean_title(rawTitle):
    """
    Cleans title of webpage, removing large spaces and junk while
    preserving valid punctuation, numbers, and capitalization.
    TO IMPROVE
    """
    deslashedTitle = re.sub(slashMatcher, "", rawTitle)
    spacedTitle = re.sub(spaceMatcher, " ", deslashedTitle).strip()
    return spacedTitle


def clean_linkSting(rawURL):
    """
    Cleans url by stripping punctuation and removing http, www, com, etc.
    Not to be confused with urlAnalyzer.clean_url!
    """
    strippedURL = re.sub(stripMathcer, "", rawURL)
    cleanedURL = re.sub(urlMathcer, "", rawURL)
    return cleanedURL


def end_test(rawString):
    """ Adds space before sentence-ending punctuation. Not yet used. """
    return re.sub(r"(?<=[a-zA-z])(?P<punc>[.!?])(?=\s[A-Z])", " \g<punc>", rawString)
