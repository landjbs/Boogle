"""
Implements functions for cleaning text for both specialized (eg. knowledge
tokenization, doc vec training) and broad (eg. pageString cleaning) purposes.
This search engine is built around the desire to store comprehensive search
results as concisely as possible, a philosophy extends to my text
processing: everything that can be removed without interfering with search
result, should be.
First iteration actions:
    -clean_text(): Primarily used to clean pageStrings before analysis
        -Replace \t, \n, and multiple spaces with a single space
        -Remove non-alpha characters
        -Lowercase all alpha characters
"""

import re

## Matchers ##
# matcher for things that look like html tags
tagMatcher = re.compile(r"<[^\s][^<]+>")

# matcher for non-alpha or space characters
stripMatcher = re.compile(r"[^a-zA-Z\s\t\t-]")

# matcher for any sequence of tabs, newlines, multiple spaces, and dashes
spaceMatcher = re.compile(r"[\t|\n|\s|-]+")

## Funcitons ##
def clean_text(rawString):
    """
    Cleans rawString but replacing spaceMatcher and tagMatcher with a single
    space, removing non-alpha chars, and lowercasing alpha chars
    """
    # replace spaceMatcher and tagMatcher with " "
    detaggeddString = re.sub(tagMatcher, " ", rawString)
    # replace stripMatcher with ""
    cleanedString = re.sub(stripMatcher, "", detaggeddString)
    # replace spaceMatcher with " " and strip surround whitespace
    spacedString = re.sub(spaceMatcher, " ", cleanedString).strip()
    # lowercase
    loweredString = spacedString.lower()
    return loweredString
