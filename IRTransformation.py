import re
from IRBuilder import *


def removeMisattributed(wikitextIR):
	misattributedRegex = re.compile('== Misattributed ==')
	rootNode = wikitextIR.getRoot()
	rootNode.removeChildrenUsingRegex(misattributedRegex)

def removeDisputed(wikitextIR):
	disputedRegex = re.compile('== Disputed ==')
	rootNode = wikitextIR.getRoot()
	rootNode.removeChildrenUsingRegex(disputedRegex)

def removeQuotesAboutX(wikitextIR):
	aboutXRegex = re.compile('== Quotes about [a-zA-Z\s]+ ==')
	rootNode = wikitextIR.getRoot()
	rootNode.removeChildrenUsingRegex(aboutXRegex)

def removeTranslations(wikitextIR):
	rootNode = wikitextIR.getRoot()
	quotesRegex = re.compile('== Quotes ==')
	translationRegex = re.compile('\s\'\'[a-zA-Z\.]')
	def matchTranslationFunction(node):
		nodeString = node.getString()
		nodeChildren = node.getChildren()
		return nodeString.startswith("* ") and len(nodeChildren) >= 2 and translationRegex.search(nodeString)
	def fixNode(nodeTranslated):
		children = nodeTranslated.getChildren()
		firstChild = children[0]
		newString = firstChild.getString()
		newString = newString[1:] # drop the first '*'
		nodeTranslated.setString(newString)
		nodeTranslated.removeChild(firstChild)
	quotesSubnodes = rootNode.findChildrenUsingRegex(quotesRegex)
	numSubnodes = len(quotesSubnodes)
	if numSubnodes > 1:
		raise InvalidWikitext("There is more than one \"QUOTES\" section. Such a format is not supported")
	elif numSubnodes == 0:
		raise InvalidWikitext("No \"QUOTES\" section found. Please contact developer")
	else:
		quotesNode = quotesSubnodes[0]
		translatedNodes = quotesNode.findChildrenUsingFunction(matchTranslationFunction)
		for nodeTranslated in translatedNodes:
			fixNode(nodeTranslated)

def removeNoiseQuotes(wikitextIR):
	removeMisattributed(wikitextIR)
	removeDisputed(wikitextIR)
	removeQuotesAboutX(wikitextIR)

def removeSections(wikitextIR):
	sectionsRegex= re.compile('== [a-zA-Z0-9\s]+ ==')
	rootNode = wikitextIR.getRoot()
	rootNode.removeNodesUsingRegex(sectionsRegex)

def removeSecondDepth(wikitextIR):
	rootNode = wikitextIR.getRoot()
	children = rootNode.getChildren()
	for child in children:
		child.removeChildren()

def removeLeadingStars(wikitextIR):
	def cleaningFunction(node):
		string = node.getString()
		newString = string.lstrip('* ')
		node.setString(newString)
	rootNode = wikitextIR.getRoot()
	rootNode.doForAllAncestry(cleaningFunction)

def cleanIR(wikitextIR):
	removeSections(wikitextIR)
	removeSecondDepth(wikitextIR)
	removeLeadingStars(wikitextIR)

def main():
	with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikitext = Wikitext(externalJSONContent)
		irinstance = WikitextIR(wikitext)
		removeNoiseQuotes(irinstance)
		removeTranslations(irinstance)
		cleanIR(irinstance)
		print irinstance.toString()

if __name__ == '__main__':
	main()
