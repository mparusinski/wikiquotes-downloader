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

class WikitextIRNode:
	"""Defines a node in the internal representation of a wikitext page"""
	def __init__(self, currentString, parentNode = None):
		self.currentString = currentString
		self.children = []
		self.parentNode = parentNode

	def addChild(self, wikitextIRNode):
		self.children.append(wikitextIRNode)

	def getParent(self):
		return self.parentNode

	def getChildren(self):
		return self.children

	def toStringList(self, tabulation):
		"""Build a list of strings"""
		firstItem = tabulation + self.currentString
		accum = [firstItem]
		for child in self.children:
			childStringList = child.toStringList(tabulation + "  ")
			accum = accum + childStringList
		return accum


class WikitextIR:
	"""Defines an internal representation of a wikitext page"""
	def __init__(self, wikitext):
		self.rootNode = WikitextIRNode(wikitext.getWikitextTitle())
		self.__parseText(wikitext.getWikitextString())

	def __parseText(self, textToParse):
		currentNode = self.rootNode
		currentDepth = 0
		for line in textToParse.splitlines():
			if self.__validLine(line, '*'):
				depth = self.__findDepth(line, '*')
				if depth > currentDepth: # Going deeper
					if not (depth - currentDepth == 1):
						# TODO Raise appropriate error
						print "Parse error! Line " + line + " is not invalid"
					else:
						newNode = WikitextIRNode(line[depth:], parentNode=currentNode)
						currentNode.addChild(newNode)
						currentNode = newNode
						currentDepth = depth
				else:
					dropAmount = currentDepth - depth
					for i in xrange(dropAmount):
						currentNode = currentNode.getParent()
					parentNode = currentNode.getParent()
					newNode = WikitextIRNode(line[depth:], parentNode=parentNode)
					parentNode.addChild(newNode)
					currentNode = newNode
					currentDepth = depth

	def __validLine(self, line, char):
		return len(line) > 0  and line[0] == char

	def __findDepth(self, line, charIndication):
		for idx, char in enumerate(line):
			if not char == charIndication:
				return idx
		return len(line)

	def getRoot(self):
		return self.rootNode

	def toString(self):
		stringList = self.rootNode.toStringList("")
		stringNoneFormatted = "\n".join(stringList)
		return stringNoneFormatted.encode('UTF-8')


class InvalidWikitext(Exception):

	def __init__(self, description):
		self.description = description

	def __str__(self):
		return repr(self.description)

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
		self.wikitext = pageElement["*"]

	def __extractWikitext(self, jsonString):
		try:
			jsonContent = json.loads(jsonString)
			page = self.__getAddressJSON(jsonContent, self.keyString)
			self.__processPage(page)
		except ValueError:
			raise InvalidWikitext("Not a valid JSON file")

	def __getAddressJSON(self, json, addressString):
		tokens = addressString.split('.')
		jsonContent = json
		for token in tokens:
			jsonContent = jsonContent[token]
		return jsonContent

	def getWikitextString(self):
		return self.wikitext

	def getWikitextTitle(self):
		return self.pageTitle

def main():
	with open('Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikitext = Wikitext(externalJSONContent)
		irinstance = WikitextIR(wikitext)
		print irinstance.toString()

if __name__ == "__main__":
	main()
		