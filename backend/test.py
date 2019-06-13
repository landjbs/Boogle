import models.knowledge.knowledgeFinder as knowledgeFinder
import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
import models.binning.docVecs as docVecs
import crawlers.htmlAnalyzer as htmlAnalyzer

from flashtext import KeywordProcessor

knowledgeSet = {'harvard'}

knowledgeProcessor = knowledgeBuilder.build_knowledgeProcessor(knowledgeSet)

db = Thicctable(knowledgeSet)

imdbModel = load('data/outData/binning/imdbModel.sav')

urlList = []
docList = [docVecs.vectorize_document(htmlAnalyzer.get_pageText(url), imdbModel) for url in urlList]
