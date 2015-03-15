import json
from StringIO import StringIO

def inspectJSONObject(json):
	for key in json.iterkeys():
		stringObjectValue = unicode(json[key])
		print key + ": " + stringObjectValue[0:100]

def inspectJSONList(json):
	for elem in json:
		stringElem = unicode(elem)
		print stringElem[0:100]

def getAddressJSON(json, addressString):
	tokens = addressString.split('.')
	jsonContent = json
	for token in tokens:
		jsonContent = jsonContent[token]
	return jsonContent

class AbstractProcessor:
	"""
	Abstract class which represents a processing function
	The function will process various steps in the conversion of a page obtained from Wikiquotes to a list of quotes
	"""
	def __init__(self, stepName):
		self.stepName = stepName

	def process(self, input):
		print "AbstractProcessor used"
		return None

class WikiquoteIRNode:
	"""Node containing a quote (hopefully) and metadata"""
	def __init__(self, ):
		self.currentString = None
		self.children = []
		self.metadataAttributes = []

class WikiquoteIR:
	"""Internal representation of a wikiquote page"""
	def __init__(self):
		self.nodes = []
		self.keyString = "query.pages"
		self.pageTitle = None

	def __processWikitext(self, wikitext):
		return wikitext

	def __processInternal(self, pageElement):
		wikitext = pageElement["*"]
		return self.__processWikitext(wikitext)

	def __processPage(self, page):
		pageKeys = page.keys()
		pageID = pageKeys[0]
		pageInternal = page[pageID]
		self.pageTitle = pageInternal['title']
		pageContent = pageInternal['revisions']
		return self.__processInternal(pageContent[0])

	def extractWikitext(self, jsonString):
		jsonContent = json.loads(jsonString)
		page = getAddressJSON(jsonContent, self.keyString)
		return self.__processPage(page)

	def populateFromJSON(self, jsonString):
		wikitext = self.extractWikitext(jsonString)
		print wikitext

def main():
	with open('Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikiquoteIR = WikiquoteIR()
		wikiquoteIR.populateFromJSON(externalJSONContent)

if __name__ == "__main__":
	main()
		