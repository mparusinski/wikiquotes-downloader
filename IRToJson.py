from IRBuilder import *
from IRTransformation import *

def makeValidityChecks(wikitextIR):
	# TODO Implement this function first
	return True

def createJSONFromIR(wikitextIR):
	tab = "  "
	jsonString = "{\n" + tab + "\"quotes\": ["
	if makeValidityChecks(wikitextIR):
		rootNode = wikitextIR.getRoot()
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
	else:
		# TODO Do it here
		print "Horrible error to throw here"

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
		jsonString = createJSONFromIR(irinstance)
		print jsonString

if __name__ == '__main__':
	main()
