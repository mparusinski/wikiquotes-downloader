# coding=UTF-8
from IRBuilder import *
from IRTransformation import *
from CleanIR import *

class IRNotReady(Exception):

	def __init__(self, detectedIssue):
		self.detectedIssue = detectedIssue

	def __str__(self):
		return repr(self.detectedIssue)


def createJSONFromIR(wikitextIR):
	tab = "  "
	jsonString = "{\n" + tab + "\"quotes\": ["
	rootNode = wikitextIR.getRoot()
	if rootNode == None:
		raise IRNotReady("No root node in IR")
	author = rootNode.getString()
	children = rootNode.getChildren()
	stringList = []
	for child in children:
		quoteText = child.getString()
		quoteString = tab + tab + "{\n" + tab + tab + tab + "\"quoteText\": \"" + quoteText + "\","
		quoteString = quoteString + "\n" + tab + tab + tab + "\"philosopher\": \"" + author + "\"\n" + tab + tab + "}"
		stringList.append(quoteString)
	internalString = ",\n".join(stringList)
	jsonString = jsonString + internalString + "\n" + tab + "]\n}\n"
	return jsonString


def main():
	with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
		externalJSONContent = filehandle.read()
		wikitext = Wikitext(externalJSONContent)
		irinstance = WikitextIR(wikitext)
		# Technically they should work on both on the same instance
		removeNoiseQuotes(irinstance)
		removeTranslations(irinstance)
		cleanIR(irinstance)
		jsonString = createJSONFromIR(irinstance)
		print jsonString

if __name__ == '__main__':
	main()
