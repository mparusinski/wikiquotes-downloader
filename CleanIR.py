# coding=UTF-8
import re
from IRBuilder import *
from DetectLanguage import *

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

def removeNoiseSections(wikitextIR):
	"""Remove sections that have nothing to do with quotes"""
	noiseSections = re.compile('== See also ==')
	rootNode = wikitextIR.getRoot()
	rootNode.removeChildrenUsingRegex(noiseSections)

def fixTranslation(translatedNode):
	children = translatedNode.getChildren()
	firstChild = children[0]
	newString = firstChild.getString()
	newString = newString[1:] # drop the first '*'
	translatedNode.setString(newString)
	translatedNode.removeChild(firstChild)

def removeTranslations(wikitextIR):
	languageDetector = LanguageDetector()
	def detectTranslation(node):
		return not languageDetector.detectLanguage(node.getString()) == "English"
	rootNode = wikitextIR.getRoot()
	quotesRegex = re.compile('== Quotes ==')
	quotesSubnodes = rootNode.findChildrenUsingRegex(quotesRegex)
	numSubnodes = len(quotesSubnodes)
	if numSubnodes > 1:
		raise InvalidWikitext("There is more than one \"QUOTES\" section. Such a format is not supported")
	elif numSubnodes == 0:
		raise InvalidWikitext("No \"QUOTES\" section found. Please contact developer")
	else:
		quotesNode = quotesSubnodes[0]
		quotesNode.getString()
		translatedNodes = quotesNode.findChildrenUsingFunction(detectTranslation)
		for nodeTranslated in translatedNodes:
			fixTranslation(nodeTranslated)

def removeNoise(wikitextIR):
	removeMisattributed(wikitextIR)
	removeDisputed(wikitextIR)
	removeQuotesAboutX(wikitextIR)
	removeNoiseSections(wikitextIR)

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

def removeQuoteDelimiters(wikitextIR):
	def cleaningFunction(node):
		string = node.getString()
		newString = string.lstrip("'")
		newString = newString.rstrip("'")
		node.setString(newString)
	rootNode = wikitextIR.getRoot()
	rootNode.doForAllAncestry(cleaningFunction)

def cleanIR(wikitextIR):
	removeSections(wikitextIR)
	removeSecondDepth(wikitextIR)
	removeLeadingStars(wikitextIR)
	removeQuoteDelimiters(wikitextIR)

def main():
	with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikitext = Wikitext(externalJSONContent)
		irinstance = WikitextIR(wikitext)
		removeNoise(irinstance)
		removeTranslations(irinstance)
		cleanIR(irinstance)
		print irinstance.toString()

if __name__ == '__main__':
	main()
