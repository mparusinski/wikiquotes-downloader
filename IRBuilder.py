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

class Wikitext:
	"""Wikitext that is embedded in a jsonString"""
	def __init__(self, jsonString):
		self.nodes = []
		self.keyString = "query.pages"
		self.pageTitle = None
		self.wikitext = None
		self.__extractWikitext(jsonString)

	def __processPage(self, page):
		pageKeys = page.keys()
		pageID = pageKeys[0]
		pageInternal = page[pageID]
		self.pageTitle = pageInternal['title']
		pageContent = pageInternal['revisions']
		pageElement = pageContent[0]
		wikitext = pageElement["*"]
		self.wikitext = wikitext.encode('UTF-8')

	def __extractWikitext(self, jsonString):
		jsonContent = json.loads(jsonString)
		page = self.__getAddressJSON(jsonContent, self.keyString)
		self.__processPage(page)

	def __getAddressJSON(self, json, addressString):
		tokens = addressString.split('.')
		jsonContent = json
		for token in tokens:
			jsonContent = jsonContent[token]
		return jsonContent

	def getWikitextString(self):
		return self.wikitext

def main():
	with open('Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikiquoteIR = WikiquoteIR()
		wikiquoteIR.buildFromJSON(externalJSONContent)

if __name__ == "__main__":
	main()
		