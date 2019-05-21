import re

def txt_to_string(pageText):
    """ Converts txt file to string """
    with open(pageText, 'r') as FileObj:
        pageString = ''
        for line in FileObj:
            assert (isinstance(line, str)), ".txt lines must have type str"
            pageString += line
        return pageString

# def find_meta(pageString):
#     """ Returns the metadata of a page as a dict """


# find_meta('samplePage.txt')
