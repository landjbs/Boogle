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
# matcher for elements to convert to spaces
spaceString = r"[\t|\n]"
spaceMatcher = re.compile(spaceString)

# matcher for elements to replace with "" in rawToken
stripString = '[(|)|.|!|?|,|\[|\]|\/|\{|\}|\n|=|$|*|+|"|®|;|^' + r".\\" + "|']"
stripMatcher = re.compile(stripString)

## Funcitons ##
def clean_text(rawString):
    """ Cleans rawToken by stripping parentheses and replacing _ with spaces """
    # replace spaceMathcer with " " in cleanToken
    spacedString = re.sub(spaceMatcher, " ", rawString)
    # replace stripMatcher with "" in rawString
    cleanedString = re.sub(stripMatcher, "", spacedString)
    # lowercase rawString
    loweredString = cleanedString.lower()
    return loweredString


while True:
    raw = input("Text: ")
    clean = clean_text(raw)
    print(f"\tClean: {clean}\n\tEmpty: {clean == ' '}")
