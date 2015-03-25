from IRTransformation import *

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
		def cleaningFunction(node):
			string = node.getString()
			newString = string.lstrip('* ')
			node.setString(newString)
		self.cleaningFunction = cleaningFunction

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.doForAllAncestry(self.cleaningFunction)


class IRCleaner(AbstractIRTransformation):

	registerTransformation('cleanIR', 'IRCleaner')

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.removeSections = RemoveSections(wikitextIR)
		self.removeSecondDepth = RemoveSecondDepth(wikitextIR)
		self.removeLeadingStars = RemoveLeadingStars(wikitextIR)

	def transform(self):
		self.removeSections.transform()
		self.removeSecondDepth.transform()
		self.removeLeadingStars.transform()
