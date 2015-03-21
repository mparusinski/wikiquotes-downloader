import re
from IRBuilder import WikitextIR, Wikitext

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
		rootNode.removeChildren(self.misattributedRegex)
		return self.wikitextIR


class EliminateDisputedIRTransformation(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.disputedRegex = re.compile('== Disputed ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildren(self.disputedRegex)
		return self.wikitextIR


class EliminateQuotesAboutXIRTransformation(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.aboutXRegex = re.compile('== Quotes about [a-zA-Z\s]+ ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildren(self.aboutXRegex)
		return self.wikitextIR


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
		print irinstance.toString()

if __name__ == '__main__':
	main()
