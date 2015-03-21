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


class EliminateMisattributedIRTransformation(AbstractIRTransformation):

	def __init__(self, wikitextIR):
		super(self.__class__, self).__init__(wikitextIR)
		self.misattributedRegex = re.compile('== Misattributed ==')

	def transform(self):
		rootNode = self.wikitextIR.getRoot()
		rootNode.removeChildren(self.misattributedRegex)
		return self.wikitextIR

def main():
	with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikitext = Wikitext(externalJSONContent)
		irinstance = WikitextIR(wikitext)
		transformer = EliminateMisattributedIRTransformation(irinstance)
		irinstance = transformer.transform()
		print irinstance.toString()

if __name__ == '__main__':
	main()
