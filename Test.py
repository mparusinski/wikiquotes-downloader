import unittest
import subprocess

from WikiquotesRetriever import WikiquotesRetriever

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

def main():
	unittest.main()

if __name__ == "__main__":
	main()