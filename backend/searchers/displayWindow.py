import operator
import re


def bold_and_window(tokenList, text, windowSize=200):
    """ Gets relevant window from pageText and bolds search tokens """
    # create matcher for all tokens in tokenList
    tokenString = ""
    for token in tokenList:
        tokenString += r"\b{}\b|".format(token)
    tokenString = tokenString[:-1]

    # find list of positions of all starting locs of tokens in text
    startList = [elt.span()[0] for elt in re.finditer(tokenString, text, flags=re.IGNORECASE)]

    def score_loc(loc):
        """ Finds number of tokens that start within windowSize of loc """
        end = loc + windowSize
        # find number of starts that are in window startin at current start
        curScore = len([otherStart for otherStart in startList if otherStart in range(loc, end)])
        return curScore

    # create dict mapping each starting location to its score
    scoredLocs = {start:score_loc(start) for start in startList}

    # find location with the highest score if there is one, else start at the beginning
    if scoredLocs != {}:
        bestLoc = max(scoredLocs.items(), key=operator.itemgetter(1))[0]
        bestStart = max(0, bestLoc-10)
    else:
        bestStart = 0

    bestEnd = bestStart + windowSize
    # get string of text within window size of bestStart
    windowText = text[bestStart : bestEnd]

    # add ellipses to beginning of windowText if bestStart isn't the beginning
    if not (bestStart<=0):
        windowText = "..." + windowText
    # add ellipses to end of windowText if bestEnd isn't the end
    if not (bestEnd>=len(text)):
        windowText += "..."

    # sub token matches for token surrounded by <strong> tags
    boldedText = re.sub(f"(?P<token>{tokenString})", "<strong>\g<token></strong>", windowText, flags=re.IGNORECASE)

    return boldedText
