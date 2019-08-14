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
from unidecode import unidecode

## Matchers ##
# matches things that look like a single html tag
tagMatcher = re.compile(r"<[^\s][^<]*>")
# matches non-alphanumeric, space, or sentence-ending punctuation (dash must be at end)
stripMatcher = re.compile(r'[^0-9a-zA-Z\t\n\s_.?!:;/<>*&^%$#@()"~`+-]')
# matches any sequence of tabs, newlines, spaces, underscores, and dashes
spaceMatcher = re.compile(r'[\t\n\s_.?!:;/<>*&^%$#@()"~`+-]+')
# matches for special wiki words like '(disambiguation)'
wikiMatcher = re.compile(r"(disambiguation)")
# matches \t \r and \n in titles
slashMatcher = re.compile(r".\r|.\n|.\t")
# matches for special parts of url
urlMatcher = re.compile(r"https|http|www|com|org|edu|.en")
# matches for the end of files
fileMatcher = re.compile(r"\.\S+")
# matcher for search spacing; identical to spaceMatcher, but " are preserved
searchSpaceMatcher = re.compile(r'[\t\n\s_.?!:;/<>*&^%$#@()~`+-]+')

# converts anything that looks like a year range (eg. 1910-11) into two years (eg. 1910 1911)
# rangedString = re.sub(r'\b(?P<firstTwo>[0-9]{2})(?P<secondTwo>[0-9]{2})-(?P<lastTwo>[0-9]{2}) ', "\g<firstTwo>\g<secondTwo> \g<firstTwo>\g<lastTwo>", dewikiedWiki)

# def convert_ordinal_number(inStr):
#     """
#     Converts ordinal numbers (eg. 1st) to their english
#     representation (eg. first)
#     """
#


## Functions ##
def clean_text(rawString):
    """
    Cleans rawString by replacing spaceMatcher and tagMatcher with a single
    space, removing non-alpha chars, and lowercasing alpha chars
    """
    # replace accented characters with non-accent representation
    deaccentedString = unidecode(rawString)
    # replace stripMatcher with ""
    cleanedString = re.sub(stripMatcher, "", rawString)
    # replace spaceMatcher with " " and strip surround whitespace
    spacedString = re.sub(spaceMatcher, " ", cleanedString).strip()
    # lowercase the alpha chars that remain
    loweredString = spacedString.lower()
    return loweredString


def clean_web_text(rawWebText):
    """ Cleans web text by removing tags and then feeding into clean_text """
    # replace html tags with " "
    detaggedString = re.sub(tagMatcher, " ", rawWebText)
    return clean_text(detaggedString)


def clean_wiki(rawWiki):
    """
    Cleans wikipedia title during knowledgeSet construction. Wraps clean_text
    but removes special wikipedia words like '(disambiguation)'.
    """
    # remove special wiki words
    dewikiedWiki = re.sub(wikiMatcher, "", rawWiki)
    # use clean_text to do the rest
    cleanedWiki = clean_text(dewikiedWiki)
    return cleanedWiki


def clean_title(rawTitle):
    """
    Cleans title of webpage, removing large spaces and junk while
    preserving valid punctuation, numbers, and capitalization.
    TO IMPROVE
    """
    deslashedTitle = re.sub(slashMatcher, "", rawTitle)
    spacedTitle = re.sub(spaceMatcher, " ", deslashedTitle).strip()
    return spacedTitle


def clean_url(rawURL):
    """
    Cleans url for knowledge tokenization by stripping punctuation and removing
    http, www, com, etc. Not to be confused with urlAnalyzer.fix_url!
    """
    cleanedURL = re.sub(urlMatcher, "", rawURL)
    strippedURL = re.sub(stripMatcher, "", cleanedURL)
    return strippedURL


def clean_file_name(rawFileName):
    """ Cleans name of a file """
    detypedFileName = re.sub(fileMatcher, "", rawFileName)
    return clean_text(detypedFileName)


### SEARCH CLEANERS ###
# dictionary to find english form of punctuation in search conversion
puncDict = {'.':'period', ',':'comma', '!':'exclamation mark',
            '?':'question mark', '...':'ellipses', '"':'quotation mark',
            "'":'appostrophe', ':':'colon', ';':'semicolon', '&':'ampersand',
            '=':'equals', '{':'bracket', '}':'bracket', '+':'plus', '-':'minus',
            '=':'equals','~':'tilda', '$':'dollar sign',
            '[':'square bracket', ']':'square bracket', '%':'percent',
            '_':'underscore'}

puncDict = {'.':'period'}


puncMatcher = re.compile(("|".join([punc for punc in puncDict.keys()])))

def clean_search(rawSearch):
    """
    Cleans search for spelling correction and tokenization.
    Wraps clean_text, but solo punctuation is converted to english
    form rather than removed (eg. : meaning -> colon meaning)
    """
    # to fix
    # puncSubbed = re.sub(r"?P<punc>{puncMatcher}", puncDict['\g<punc>'], rawSearch)
    # replace stripMatcher with ""
    cleanedString = re.sub(stripMatcher, "", rawSearch)
    # replace spaceMatcher with " " and strip surround whitespace
    spacedString = re.sub(searchSpaceMatcher, " ", cleanedString).strip()
    # lowercase the alpha chars that remain
    loweredString = spacedString.lower()
    return loweredString


def end_test(rawString):
    """ Adds space before sentence-ending punctuation. Not yet used. """
    return re.sub(r"(?<=[a-zA-z])(?P<punc>[.!?])(?=\s[A-Z])", " \g<punc>", rawString)
