# coding=UTF-8
import unittest
import os
import sys
import re
import subprocess
import copy

from WikiquotesRetriever import *
from IRBuilder import *
from IRTransformation import *
from DetectLanguage import *

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

class TestDetectLanguage(unittest.TestCase):

	def testFindEnglishSentence(self):
		englishScore = matchLanguage("Once upon a time there was a sausage called Baldrick", commonWordsEnglish)
		frenchScore = matchLanguage("Il etait une fois une saucisse nomme Baldrick", commonWordsEnglish)
		self.assertTrue(englishScore > frenchScore)

	def testDetectEnglish(self):
		englishSentence = "Once upon a time there was a sausage called Baldrick"
		self.assertTrue(detectLanguage(englishSentence) == "English")

	def testDetectGerman(self):
		germanQuote = "Man verdirbt einen Jüngling am sichersten, wenn man ihn anleitet, den Gleichdenkenden höher zu achten, als den Andersdenkenden."
		self.assertTrue(detectLanguage(germanQuote) == "German")

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
			removeDisputed(wikitextIR)
			with open('baselines/Friedrich_Nietzsche_no_disputed.wikitextIR', 'w') as writehandle:
				writehandle.write(wikitextIR.toString())

	def rebuildForTestCorrectMisattributedRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			removeMisattributed(wikitextIR)
			with open('baselines/Friedrich_Nietzsche_no_misattributed.wikitextIR', 'w') as writehandle:
				writehandle.write(wikitextIR.toString())

	def rebuildForTestCorrectQuoteAboutXRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			removeQuotesAboutX(wikitextIR)
			with open('baselines/Friedrich_Nietzsche_no_quotes_about_x.wikitextIR', 'w') as writehandle:
				writehandle.write(wikitextIR.toString())


class IRTransformationsTest(unittest.TestCase):

	def testCorrectDisputedRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			removeDisputed(wikitextIR)
			with open('baselines/Friedrich_Nietzsche_no_disputed.wikitextIR', 'r') as baselineFileHandle:
				baseline = baselineFileHandle.read()
				self.assertTrue(baseline == wikitextIR.toString())

	def testCorrectMisattributedRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			removeMisattributed(wikitextIR)
			with open('baselines/Friedrich_Nietzsche_no_misattributed.wikitextIR', 'r') as baselineFileHandle:
				baseline = baselineFileHandle.read()
				self.assertTrue(baseline == wikitextIR.toString())

	def testCorrectQuoteAboutXRemoval(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIR = WikitextIR(wikitext)
			removeQuotesAboutX(wikitextIR)
			with open('baselines/Friedrich_Nietzsche_no_quotes_about_x.wikitextIR', 'r') as baselineFileHandle:
				baseline = baselineFileHandle.read()
				self.assertTrue(baseline == wikitextIR.toString())

	def testRemoversCommute(self):
		with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
			externalJSONContent = filehandle.read()
			wikitext = Wikitext(externalJSONContent)
			wikitextIRLeft = WikitextIR(wikitext)
			wikitextIRRight = copy.deepcopy(wikitextIRLeft)
			removeMisattributed(wikitextIRLeft)
			removeDisputed(wikitextIRLeft)
			removeDisputed(wikitextIRRight)
			removeMisattributed(wikitextIRRight)
			self.assertTrue(wikitextIRLeft.toString() == wikitextIRRight.toString())


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
