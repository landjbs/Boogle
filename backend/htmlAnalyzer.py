import re

def txt_to_string(pageText):
    """ Converts txt file to string """
    with open(pageText, 'r') as FileObj:
        # create string of joined lines in .txt file
        pageString = "".join(line for line in FileObj)
        return pageString

def find_meta(pageString, metaParams):
    """
    Args: string of decoded page text, list of parameters to grab
    Returns: metadata of pageString as a dict mapping metaParams to values
    """
    # find all meta tags in pageString
    metaList = re.findall("(?<=<meta )" + ".+" + "(?=>)", pageString)
    # find all individual tags within metaList
    tagString = "(?<=<meta )" + ".+" + "=" + ".+" + '(?=<")' + '(?=")' + "." + "(?=>)"
    tagList = re.findall(tagString, pageString)

    # find_tag = lambda t : t
    #
    # tagList = list(map(find_tag, metaList))
    #
    # print(tagList)

    # def meta_to_dict(metaList):
    #     """ Converts singmeta list to dict """



sample_pageString = txt_to_string('samplePage.txt')

print(sample_pageString)

# find_meta(sample_pageString)
