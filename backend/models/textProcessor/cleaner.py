import re

## Matchers ##
# matcher for elements to replace with "" in rawToken
stripString = '[(|)|.|!|?|,|\[|\]|\/|\{|\}|\n|=|$|*|+|"|®|;' + r".\\" + "|']"
stripMatcher = re.compile(stripString)
# matcher for elements to convert to spaces
spaceString = r"[_]"
spaceMatcher = re.compile(spaceString)

## Funcitons ##
def clean_knowledgeToken(rawString):
    """ Cleans rawToken by stripping parentheses and replacing _ with spaces """
    # lowercase rawString
    loweredString = rawString.lower()
    # replace stripMatcher with "" in rawString
    cleanedString = re.sub(stripMatcher, "", loweredString)
    # replace spaceMathcer with " " in cleanToken
    spacedString = re.sub(spaceMatcher, " ", cleanedString)
    return spacedString
