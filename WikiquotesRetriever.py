import pycurl
import json
from StringIO import StringIO

class WikiquotesRetriever():
	"""This class retrieves pages from Wikiquotes"""
	def __init__(self):
		self.titlePlaceholder   = "%%TITLE%%"
		self.wikiquoteurlformat = "http://en.wikiquote.org/w/api.php?format=json&action=query&titles=" \
			+ self.titlePlaceholder + "&prop=revisions&rvprop=content"
		self.curler = None

	def setupNetworking(self):
		self.curler = pycurl.Curl()

	def closeNetworking(self):
		self.curler.close()

	def __preprocessTitle(self, title):
		""" For instance "Friedrich Nietzsche" would become "Friedrich_Nietzsche" """
		return title.replace(' ','%20')

	def __getURL(self, title):
		urlReadyTitle = self.__preprocessTitle(title)
		urlForTitle = self.wikiquoteurlformat.replace(self.titlePlaceholder, urlReadyTitle)
		return urlForTitle

	def downloadQuote(self, title):
		buffer = StringIO()
		self.curler.setopt(self.curler.URL, self.__getURL(title))
		self.curler.setopt(self.curler.WRITEDATA, buffer)
		self.curler.perform()
		return buffer.getvalue()

def main():
	wikiRetriever = WikiquotesRetriever()
	wikiRetriever.setupNetworking()
	print wikiRetriever.downloadQuote("Friedrich Nietzsche")
	wikiRetriever.closeNetworking()

# def main():
# 	curler = pycurl.Curl()
# 	body = downloadQuote(curler, "Friedrich Nietzsche")
# 	jsonObject = json.loads(body)
# 	for key in jsonObject.iterkeys():
# 		print key
# 	curler.close()

if __name__ == '__main__':
	main()
