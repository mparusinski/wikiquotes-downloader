import unittest
import os
import sys
import subprocess

from WikiquotesRetriever import *
from IRBuilder import *

REBUILDBASELINES = True

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


class WikitextIRBaselines:

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


class WikitextExtractorBaselines:
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


class WikiquotesRetrieverBaselines:
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
	wikiquotesRetrieverBaselines = WikiquotesRetrieverBaselines()
	wikiquotesRetrieverBaselines.rebuildForTestCorrectJSONDownloaded()
	wikitextExtractorBaselines = WikitextExtractorBaselines()
	wikitextExtractorBaselines.rebuildForTestCorrectWikitextBuilt()
	wikitextIRBaselines = WikitextIRBaselines()
	wikitextIRBaselines.rebuildForTestCorrectWikitextIR()


def main():
	if REBUILDBASELINES:
		rebuildBaselines()
	else:
		unittest.main()

if __name__ == "__main__":
	main()
