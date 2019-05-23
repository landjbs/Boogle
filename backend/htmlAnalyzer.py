import re

def txt_to_string(pageText):
    """ Converts txt file to string """
    with open(pageText, 'r') as FileObj:
        # create string of joined lines in .txt file
        pageString = "".join(line for line in FileObj)
        return pageString

# def find_meta(pageString, paramList):
#     """
#     Args: string of decoded page text, list of parameters to grab
#     Returns: metadata of pageString as a dict mapping metaParams to values
#     """
#     # find contents of all meta tags in pageString
#     metaList = re.findall("(?<=<meta )" + ".+" + "(?=>)", pageString)
#
#     def paramMatcher(elt, paramList=paramList):
#         """ Matches metaParams in elt of metaList """
#         param_matchString = f"{[paramList]}" + ".+" + "=" + ".+"
#         paramList = re.findall(param_matchString, elt)
#         return paramList
#
#     # find all individual params within metaList
#     paramString = list(map(lambda elt : paramMatcher(elt), metaList))
#
#
#     def meta_to_dict(metaList):
#         """ Converts meta list to dict """
#
#
# sample_pageString = txt_to_string('samplePage.txt')
#
# print(sample_pageString)
#
# find_meta(sample_pageString)

def find_links(pageString):
    """ Find urls contained by all <a href=""> tags """
    # href_matchString = '(?<=href=")' + ".+" + '(?=")'
    href_matchString2 = 'https://' + "\S+" + '(?=")'
    urlList = re.findall(href_matchString2, pageString)
    return urlList
