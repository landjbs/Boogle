import re

# matcher for text in <title></title> tags, ignoring case
titleString = r'(?<=<title>).+(?=</title>)'
titleMatcher = re.compile(titleString, re.IGNORECASE)

# matcher for links denoted by https:// or http://
linkString = r'https://\S+(?=")|http://\S+(?=")'
linkMatcher = re.compile(linkString)

# matcher for everything in <body></body> tags
bodyString = r'(?<=<body).+(?=</body>)'
bodyMatcher = re.compile(bodyString, re.IGNORECASE)



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


with open('../data/practiceWeb.txt', 'r') as FileObj:
    text = "".join(line for line in FileObj)

x = titleMatcher.findall(text)

print(x)
