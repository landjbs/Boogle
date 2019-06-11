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
# matcher for any sequence of tabs, newlines, multiple spaces, and dashes
spaceString = r"[\t|\n|\s|-]+"
spaceMatcher = re.compile(spaceString)

# matcher for things that look like html tags
tagString = r"(?<=<[^\s])[^<]+(?=>)"
tagMatcher = re.compile(tagString)

# matcher for non-alpha or space characters
stripString = r"[^a-zA-Z\s]"
stripMatcher = re.compile(stripString)

## Funcitons ##
def clean_text(rawString):
    """ Cleans rawToken by stripping parentheses and replacing _ with spaces """
    # replace spaceMatcher and tagMatcher with " "
    spacedString = re.sub(tagMatcher, " ", re.sub(spaceMatcher, " ", rawString))
    # replace stripMatcher with "" in rawString and remove trailing whitespace
    cleanedString = re.sub(stripMatcher, "", spacedString).strip()
    # lowercase rawString
    loweredString = cleanedString.lower()
    return loweredString


while True:
    raw = input("Text: ")
    clean = clean_text(raw)
    print(clean)
