import re

def find_title(pageString):
    """ Find title of an html page """
    title_matchString = "(?<=<title>)" + ".+" + "(?=</title>)"
    titleList = re.findall(title_matchString, pageString)
    return titleList

def find_links(pageString):
    """ Find urls contained by all <a href=""> tags """
    # href_matchString = '(?<=href=")' + ".+" + '(?=")'
    # match for https:// followed by anything but space followed by "
    href_matchString = 'https://' + "\S+" + '(?=")'
    urlList = re.findall(href_matchString, pageString)
    return urlList

def find_descriptions(pageString):
    """ Find meta tags with description name """
    description_matchString = '(?<=(name="description" content="))' + 'content="' + ".+" + '(?=")'
    descriptionList = re.findall(description_matchString, pageString)
    return descriptionList

def find_images(pageString):
    """ Find images contained in pageString """
    img_matchString = '(?<=src=")' + "\S+" + '(?=")'
    imgList = re.findall(img_matchString, pageString)
    return imgList

def vectorize_paragraph(pageString):
    """ Converts page html into vector for modeling (inpsired by
        https://cs.stanford.edu/~quocle/paragraph_vector.pdf)"""
    
