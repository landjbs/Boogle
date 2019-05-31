import re

# matcher for text in <title></title> tags
titleString = r'(?<=<title>).+(?=</title>)'
titleMatcher = re.compile(titleString)

# matcher for links denoted by https:// or http://
linkString = r'https://\S+(?=")|http://\S+(?=")'
linkMatcher = re.compile(linkString)

# matcher for everything in <body></body> tags
bodyString = r'(?=<body>).+(?=</body>)'

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


text = '<title>Harvard University</title>'

x = titleMatcher.findall(text)

# x = re.match(r'.+', text)


print(x)

#
# x = re.findall(testMatch, text)
#
# print(x)
