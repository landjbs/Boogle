import re

def txt_to_string(pageText):
    """ Converts txt file to string """
    with open(pageText, 'r') as FileObj:
        # create string of joined lines in .txt file
        pageString = "".join(line for line in FileObj)
        return pageString

def find_meta(pageString):
    """ Returns the metadata of a page as a dict """
    # find all meta tags in pageString
    metaList = re.findall("(?<=<meta )" + ".+" + "(?=>)", pageString)
    # find all individual tags within metaList
    tagString = "(?<=<meta )" + ".+" + "=" + ".+" + '(?=<")' + '(?=")' + "." + "(?=>)"
    tagList = re.findall(tagString, pageString)


    print(tagList)

    # def meta_to_dict(metaList):
    #     """ Converts singmeta list to dict """



sample_pageString = txt_to_string('samplePage.txt')

find_meta(sample_pageString)
