import unittest
import os
import sys
import subprocess

from WikiquotesRetriever import WikiquotesRetriever, InvalidTitleException

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


class WikiquotesRetrieverBaselines:
	"""Class to rebuild baselines"""

	def rebuildForTestCorrectJSONDownloaded(self):
		quoteURL = "\"http://en.wikiquote.org/w/api.php?format=json&action=query&titles=Friedrich%20Nietzsche&prop=revisions&rvprop=content\""
		saferSystemCall('curl ' + quoteURL + ' > Friedrich_Nietzsche.json')


class WikiquotesRetrieverTest(unittest.TestCase):

	def testCorrectJSONDownloaded(self):
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		onlineJSONContent = wikiRetriever.downloadQuote("Friedrich Nietzsche")
		wikiRetriever.closeNetworking()
		with open('Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
		areEqual = externalJSONContent == onlineJSONContent
		self.assertTrue(areEqual)

	def testNotHardcodedJSONDownloaded(self):
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		onlineJSONContent = wikiRetriever.downloadQuote("Plato")
		wikiRetriever.closeNetworking()
		with open('Friedrich_Nietzsche.json', 'r') as filehandle:
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
	print "Rebuilding baselines instead of running test"
	print "Execute at your own risk"
	wikiquotesRetrieverBaselines = WikiquotesRetrieverBaselines()
	wikiquotesRetrieverBaselines.rebuildForTestCorrectJSONDownloaded()

def main():
	if REBUILDBASELINES:
		rebuildBaselines()
	else:
		unittest.main()

if __name__ == "__main__":
	main()
