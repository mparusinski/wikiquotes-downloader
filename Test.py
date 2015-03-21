import unittest
import os
import sys
import re
import subprocess

from WikiquotesRetriever import *
from IRBuilder import *
from IRTransformation import *

REBUILDBASELINES = False

def saferSystemCall(call):
	print "---------------------------------------------------------------------"
	print "The following command is to be executed"
	print "\t" + call
	validResponse = False
	while not validResponse:
		userResponse = raw_input("Do you wish to execute this command? (YES/NO) ")
		if userResponse == "YES":
			validResponse = True
			os.system(call)
		elif userResponse == "NO":
			validResponse = True
		else:
			print "Please type YES or NO!"


class BaselineBuilder(object):

	def __inheritors(self):
		return BaselineBuilder.__subclasses__()

	def runBaselinesBuilders(self):
		regex = re.compile('^rebuild')
		subclassesList = self.__inheritors()
		for subclass in subclassesList:
			subclassName = subclass.__name__
			obj = globals()[subclassName]()
			methods = [method for method in dir(subclass) if callable(getattr(obj, method))]
			for method in methods:
				if regex.match(method):
					eval(subclassName + '().' + method + '()')

class IRTransformationsBaselines(BaselineBuilder):

	def rebuildForTestCorrectDisputedRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			disputedRemover = EliminateDisputedIRTransformation(wikitextIR)
			disputedRemover.transform()
			with open('baselines/Friedrich_Nietzsche_no_disputed.wikitextIR', 'w') as writehandle:
				writehandle.write(disputedRemover.getIR().toString())

	def rebuildForTestCorrectMisattributedRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			misattributedRemover = EliminateMisattributedIRTransformation(wikitextIR)
			misattributedRemover.transform()
			with open('baselines/Friedrich_Nietzsche_no_misattributed.wikitextIR', 'w') as writehandle:
				writehandle.write(misattributedRemover.getIR().toString())

	def rebuildForTestCorrectQuoteAboutXRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			quotesAboutXRemover = EliminateQuotesAboutXIRTransformation(wikitextIR)
			quotesAboutXRemover.transform()
			with open('baselines/Friedrich_Nietzsche_no_quotes_about_x.wikitextIR', 'w') as writehandle:
				writehandle.write(quotesAboutXRemover.getIR().toString())


class IRTransformationsTest(unittest.TestCase):

	def testCorrectDisputedRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			disputedRemover = EliminateDisputedIRTransformation(wikitextIR)
			disputedRemover.transform()
			with open('baselines/Friedrich_Nietzsche_no_disputed.wikitextIR', 'r') as baselineFileHandle:
				baseline = baselineFileHandle.read()
				self.assertTrue(baseline == disputedRemover.getIR().toString())

	def testCorrectMisattributedRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			misattributedRemover = EliminateMisattributedIRTransformation(wikitextIR)
			misattributedRemover.transform()
			with open('baselines/Friedrich_Nietzsche_no_misattributed.wikitextIR', 'r') as baselineFileHandle:
				baseline = baselineFileHandle.read()
				self.assertTrue(baseline == misattributedRemover.getIR().toString())

	def testCorrectQuoteAboutXRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			quotesAboutXRemover = EliminateQuotesAboutXIRTransformation(wikitextIR)
			quotesAboutXRemover.transform()
			with open('baselines/Friedrich_Nietzsche_no_quotes_about_x.wikitextIR', 'r') as baselineFileHandle:
				baseline = baselineFileHandle.read()
				self.assertTrue(baseline == quotesAboutXRemover.getIR().toString())


class WikitextIRBaselines(BaselineBuilder):

	def rebuildForTestCorrectWikitextIR(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			with open('baselines/Friedrich_Nietzsche.wikitextIR', 'w') as writehandle:
				writehandle.write(wikitextIR.toString())


class WikitextIRTest(unittest.TestCase):

	def testCorrectWikitextIR(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			with open('baselines/Friedrich_Nietzsche.wikitextIR', 'r') as baselineFileHandle:
				baselineIR = baselineFileHandle.read()
				self.assertTrue(baselineIR == wikitextIR.toString())


class WikitextExtractorBaselines(BaselineBuilder):
	"""Class to rebuild baselines"""

	def rebuildForTestCorrectWikitextBuilt(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			with open('baselines/Friedrich_Nietzsche.wikitext', 'w') as writehandle:
				writehandle.write(wikitext.getWikitextString().encode('UTF-8'))


class WikitextExtractorTest(unittest.TestCase):

	def testCorrectWikitextBuild(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			with open('baselines/Friedrich_Nietzsche.wikitext', 'r') as readhandle:
				wikitextbaseline = readhandle.read()
				self.assertTrue(wikitext.getWikitextString().encode('UTF-8') == wikitextbaseline)

	def testOtherWikitextBuild(self):
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		onlineJSONContent = wikiRetriever.downloadQuote("Baruch Spinoza")
		wikiRetriever.closeNetworking()
		wikitext = Wikitext(onlineJSONContent)

	def testEmptyWikitext(self):
		with self.assertRaises(InvalidWikitext):
			wikitext = Wikitext("")


class WikiquotesRetrieverBaselines(BaselineBuilder):
	"""Class to rebuild baselines"""

	def rebuildForTestCorrectJSONDownloaded(self):
		quoteURL = "\"http://en.wikiquote.org/w/api.php?format=json&action=query&titles=Friedrich%20Nietzsche&prop=revisions&rvprop=content\""
		saferSystemCall('curl ' + quoteURL + ' > baselines/Friedrich_Nietzsche.json')


class WikiquotesRetrieverTest(unittest.TestCase):

	def testDownloadingVarious(self):
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		wikiRetriever.downloadQuote("Friedrich_Nietzsche")
		wikiRetriever.downloadQuote("Baruch Spinoza")
		wikiRetriever.closeNetworking()

	def testCorrectJSONDownloaded(self):
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		onlineJSONContent = wikiRetriever.downloadQuote("Friedrich Nietzsche")
		wikiRetriever.closeNetworking()
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
		areEqual = externalJSONContent == onlineJSONContent
		self.assertTrue(areEqual)

	def testNotHardcodedJSONDownloaded(self):
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		onlineJSONContent = wikiRetriever.downloadQuote("Plato")
		wikiRetriever.closeNetworking()
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
		areEqual = externalJSONContent == onlineJSONContent
		self.assertTrue(not areEqual)

	def testNonFNTitle(self):
		try:
			wikiRetriever = WikiquotesRetriever()
			wikiRetriever.setupNetworking()
			onlineJSONContent = wikiRetriever.downloadQuote("Baruch Spinoza")
			wikiRetriever.closeNetworking()
		except:
			self.fail("No exception should be thrown")

	def testInvalidTitle(self):
		with self.assertRaises(InvalidTitleException): 
			wikiRetriever = WikiquotesRetriever()
			wikiRetriever.setupNetworking()
			onlineJSONContent = wikiRetriever.downloadQuote("SpinozaBanana")
			wikiRetriever.closeNetworking()


def rebuildBaselines():
	print "!!!!Rebuilding baselines instead of running test!!!!"
	print "!!!!Execute at your own risk!!!!"
	baselineBuilder = BaselineBuilder()
	baselineBuilder.runBaselinesBuilders()

def main():
	if REBUILDBASELINES:
		rebuildBaselines()
	else:
		unittest.main()

if __name__ == "__main__":
	main()
