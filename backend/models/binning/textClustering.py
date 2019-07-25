import re
import numpy as np
from os import listdir
from scipy.spatial.distance import euclidean

from dataStructures.objectSaver import load, save

people = ['Luther Dickinson', 'T. Coraghessan Boyle', 'Georges Parfait Mbida Messi',
            'Jim Bohannon', 'Paula Raymond', 'George Jones', 'William H. Hinton', 'James Cayne', 'Mickey Munday', 'Al Corley', 'Tom Nugent', 'Pete Conrad', 'Alexis Arquette', 'Jimmy McCracklin', 'Phyllis Hyman', 'Bob Woodruff', 'Ted Cassidy', 'Scotty Beckett', 'Sparky Anderson', 'Kevin M. Connolly', 'Barney McKenna', 'James Lincoln Collier', 'Walt Kelly', 'Bob Sirott', 'George Russell Weller', 'Eddie Griffin', 'Jennifer Syme', 'Bob Denver', 'Larry Sullivan', 'Rufus Wainwright', 'Bob Benmosche', 'D. B. Sweeney', 'Tané McClure', 'Terry Balsamo', 'Lee Falk', 'Jay R. Smith', 'Johnny Cash', 'Art Barr', 'Danny Aiello', 'Terrence C. Carson', 'Michael Piller', 'T. J. Cloutier', 'Scott Adsit', 'Daniel Johnston', 'Arthur Blessitt', 'Kipp Lennon', 'Alice Playten', 'Frances Scott Fitzgerald', 'Dav Pilkey', 'Mayo A. Shattuck III', 'Graig Nettles', 'Dave Hickey', 'Chris Paciello', 'John Weinberg', 'Elizabeth George Speare', 'Cliff Edwards', 'Bowie Kuhn', 'Jack Daniel', 'Charles Douglass', 'Eugene Jackson', 'Matt Reeves', 'Allen Funt', 'Bill Laswell', 'Neal McDonough', 'Bob Goodlatte', 'Jack Dunphy', 'Neal Doughty', 'Nick Kroll', 'Steve Sabol', 'Leo Fitzpatrick', 'Thom Brennaman', 'Tina Weymouth', 'John F. Fitzgerald', 'Christopher Hitchens', 'Chuck Behler', 'Doug TenNapel', 'Michael Patrick MacDonald', 'Matthew Haughey', 'Steve Van Buren', 'Nick Gravenites', 'Paul Zindel', 'Ben Schwartzwalder', 'Jimmy Carl Black', 'Gene Wilder', 'George Crile III', 'Justin Guarini', 'Edmund Wilson', 'Foster Sylvers', 'Dan T. Cathy', 'Robert Fagles', 'Benson John Lossing', 'Wahoo McDaniel', 'Cootie Williams', 'Geena Davis', 'Frank Middlemass', 'Sue Bird', 'Montel Williams', 'Zola Taylor', 'Duff McKagan', 'Kenneth Burke', 'William Sloane Coffin', 'Jef Raskin', 'B. Todd Jones', 'Junior Wells', 'Fred Schneider']

peopleVecs = []

def cluster_file_contents(filePath, n):
    vecDict = {}
    for i, file in enumerate(listdir(filePath)):
        if i > n:
            break
        pageList = load(f'{filePath}/{file}')
        for pageDict in pageList:
            title, vec = pageDict['title'].strip(), pageDict['pageVec']
            if title in people:
                peopleVecs.append(vec)
            vecDict.update({title: vec})

    peopleAverage = np.average(peopleVecs, axis=0)
    save(peopleAverage, "data/outData/binning/averagePersonVec.sav")

    print(peopleAverage)
    rankedList = []
    for title, vec in vecDict.items():
        if not title in people:
            distance = euclidean(vec, peopleAverage)
            rankedList.append((distance, title))
    rankedList.sort()

    for elt in rankedList[1000:]:
        print(f'{elt[0]} - {elt[1]}')


def get_people_texts(filePath, cutoff=5.57):
    peopleVec = load('data/outData/binning/averagePersonVec.sav')
    for i, file in enumerate(listdir(filePath)):
        pageList = load(f'{filePath}/{file}')
        for pageDict in pageList:
            pageVec = pageDict['pageVec']
            distance = euclidean(peopleVec, pageVec)
            if distance < cutoff:
                pageText = pageDict['windowText']
                cleanedText = re.sub(r'\([^)]+\) ', '', pageText)
                print(f'\n\n{cleanedText}\n')
