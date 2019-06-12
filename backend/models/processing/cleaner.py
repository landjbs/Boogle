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
tagMatcher = re.compile(r"<[^\s][^<]+>")
# matches non-alpha or space characters (dash must be at end)
stripMatcher = re.compile(r"[^a-zA-Z\s\t\n_-]")
# matches any sequence of tabs, newlines, spaces, underscores, and dashes
spaceMatcher = re.compile(r"[\t|\n|\s|-|_]+")

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
