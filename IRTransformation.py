import re
from IRBuilder import *

class IRTransformersRegistry(object):

	def __init__(self):
		self.registry = dict()

	def addTransformer(self, transformerName, classname):
		self.registry[transformerName] = classname

	def getClassname(self, transformerName):
		return self.registry[transformerName]
	

class TransformationProcess(object):

	def __init__(self, wikitextIR):
		self.wikitextIR = wikitextIR
		self.process = []

	def applyTransformer(self, transformerName):
		self.process.append(transformerName)

	def runProcess(self):
		for transformer in self.process:
			classname = irTransformersRegistry.getClassname(transformer)
			transformer = self.__instantiate(classname)
			transformer.transform()

	def __instantiate(self, classname):
		return eval(classname + '(self.wikitextIR)') # hope this works


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


class RemoveMisattributed(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.misattributedRegex = re.compile('== Misattributed ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildrenUsingRegex(self.misattributedRegex)
		return self.wikitextIR


class RemoveDisputed(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.disputedRegex = re.compile('== Disputed ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildrenUsingRegex(self.disputedRegex)
		return self.wikitextIR


class RemoveQuotesAboutX(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.aboutXRegex = re.compile('== Quotes about [a-zA-Z\s]+ ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildrenUsingRegex(self.aboutXRegex)
		return self.wikitextIR


class RemoveTranslations(AbstractIRTransformation):

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


class RemoveSections(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.sectionsRegex= re.compile('== [a-zA-Z0-9\s]+ ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeNodesUsingRegex(self.sectionsRegex)
		return self.wikitextIR

class RemoveSecondDepth(AbstractIRTransformation):
	""" This assumes sections have been removed """

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		children = rootNode.getChildren()
		for child in children:
			child.removeChildren()

class RemoveLeadingStars(AbstractIRTransformation):
	""" This assumes sections have been removed """

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)

	def transform(self):
		def cleaningFunction(node):
			string = node.getString()
			newString = string.lstrip('* ')
			node.setString(newString)
		rootNode = self.wikitextIR.getRoot()
		rootNode.doForAllAncestry(cleaningFunction)


irTransformersRegistry = IRTransformersRegistry()
irTransformersRegistry.addTransformer('removeMisattributed', 'RemoveMisattributed')
irTransformersRegistry.addTransformer('removeDisputed', 'RemoveDisputed')
irTransformersRegistry.addTransformer('removeTranslations', 'RemoveTranslations')
irTransformersRegistry.addTransformer('removeQuotesAboutX', 'RemoveQuotesAboutX')
irTransformersRegistry.addTransformer('removeSections', 'RemoveSections')
irTransformersRegistry.addTransformer('removeSecondDepth', 'RemoveSecondDepth')
irTransformersRegistry.addTransformer('removeLeadingStars', 'RemoveLeadingStars')

def main():
	with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikitext = Wikitext(externalJSONContent)
		irinstance = WikitextIR(wikitext)
		# Technically they should work on both on the same instance
		process = TransformationProcess(irinstance)
		process.applyTransformer('removeMisattributed')
		process.applyTransformer('removeDisputed')
		process.applyTransformer('removeQuotesAboutX')
		process.applyTransformer('removeTranslations')
		process.applyTransformer('removeSections')
		process.applyTransformer('removeSecondDepth')
		process.applyTransformer('removeLeadingStars')
		process.runProcess()
		print irinstance.toString()

if __name__ == '__main__':
	main()
