import re
from IRBuilder import *

class UndefinedTransformFunction(Exception):

	def __init__(self, className):
		self.className = className

	def __str__(self):
		return repr(self.className + " does not implement the abstract function transform")

class AbstractIRTransformation(object):

	def __init__(self, wikitextIR):
		self.wikitextIR = wikitextIR

	def transform(self):
		# Starts doing the transform
		raise UndefinedTransformFunction(self.__class__.__name__)
		return None

	def getIR(self):
		return self.wikitextIR


class EliminateMisattributedIRTransformation(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.misattributedRegex = re.compile('== Misattributed ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildrenUsingRegex(self.misattributedRegex)
		return self.wikitextIR


class EliminateDisputedIRTransformation(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.disputedRegex = re.compile('== Disputed ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildrenUsingRegex(self.disputedRegex)
		return self.wikitextIR


class EliminateQuotesAboutXIRTransformation(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.aboutXRegex = re.compile('== Quotes about [a-zA-Z\s]+ ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildrenUsingRegex(self.aboutXRegex)
		return self.wikitextIR


class EliminateTranslationsTransformation(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.quotesRegex = re.compile('== Quotes ==')
		self.translationRegex = re.compile('\s\'\'[a-zA-Z\.]')
		def matchTranslationFunction(node):
			nodeString = node.getString()
			nodeChildren = node.getChildren()
			return nodeString.startswith("* ") and len(nodeChildren) >= 2 and self.translationRegex.search(nodeString)
		self.matchTranslationFunction = matchTranslationFunction

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		quotesSubnodes = rootNode.findChildrenUsingRegex(self.quotesRegex)
		numSubnodes = len(quotesSubnodes)
		if numSubnodes > 1:
			raise InvalidWikitext("There is more than one \"QUOTES\" section. Such a format is not supported")
			return self.wikitextIR
		elif numSubnodes == 0:
			raise InvalidWikitext("No \"QUOTES\" section found. Please contact developer")
			return self.wikitextIR
		else:
			quotesNode = quotesSubnodes[0]
			translatedNodes = quotesNode.findChildrenUsingFunction(self.matchTranslationFunction)
			for nodeTranslated in translatedNodes:
				self.__fixNode(nodeTranslated)
			return self.wikitextIR

	def __fixNode(self, nodeTranslated):
		children = nodeTranslated.getChildren()
		firstChild = children[0]
		newString = firstChild.getString()
		newString = newString[1:] # drop the first '*'
		nodeTranslated.setString(newString)
		nodeTranslated.removeChild(firstChild)


def main():
	with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikitext = Wikitext(externalJSONContent)
		irinstance = WikitextIR(wikitext)
		# Technically they should work on both on the same instance
		transformer1 = EliminateMisattributedIRTransformation(irinstance)
		transformer2 = EliminateDisputedIRTransformation(irinstance)
		transformer3 = EliminateQuotesAboutXIRTransformation(irinstance)
		transformer1.transform()
		transformer2.transform()
		transformer3.transform()
		translatedNodesTransformer = EliminateTranslationsTransformation(irinstance)
		translatedNodesTransformer.transform()
		print irinstance.toString()

if __name__ == '__main__':
	main()
