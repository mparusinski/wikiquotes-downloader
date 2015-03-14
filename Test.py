import unittest
from WikiquotesRetriever import WikiquotesRetriever

class WikiquotesRetrieverTest(unittest.TestCase):

	def testCorrectJSONDownloaded(self):
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		onlineJSONContent = wikiRetriever.downloadQuote("Friedrich Nietzsche")
		print onlineJSONContent
		wikiRetriever.closeNetworking()
		with open('Friedrich_Nietzsche.json', 'r') as fileHandle:
			savedJSONContent = fileHandle.read()
			self.assertTrue(savedJSONContent == onlineJSONContent)

def main():
	unittest.main()

if __name__ == "__main__":
	main()