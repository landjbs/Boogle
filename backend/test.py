import models.knowledge.knowledgeFinder as knowledgeFinder
import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
import models.binning.docVecs as docVecs
import crawlers.htmlAnalyzer as htmlAnalyzer

from flashtext import KeywordProcessor
from gensim.models.doc2vec import Doc2Vec

knowledgeSet = {'harvard'}

knowledgeProcessor = knowledgeBuilder.build_knowledgeProcessor(knowledgeSet)

db = Thicctable(knowledgeSet)

imdbModel = Doc2Vec.load('data/outData/binning/imdbModel.sav')

urlList = ['www.harvard.edu', 'https://en.wikipedia.org/wiki/Harvard_University',
            'https://simple.wikipedia.org/wiki/Harvard_University',
            'https://twitter.com/Harvard?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor',
            'https://www.hbs.edu/Pages/default.aspx', 'http://www.harvard.com']

docDict = {}

for url in urlList:
    pageText = htmlAnalyzer.get_pageText(url)
    pageVec = docVecs.vectorize_document(pageText, imdbModel)
    tokenCounts = knowledgeFinder.find_countedTokens(pageText, knowledgeProcessor)
    for token in tokenCounts:
        db.insert_value(token, [url, pageVec])
    docDict.update({url:pageVec})

docVecs.visualize_vecDict()

db.plot_lengths()







pass
