import pycurl
import json
from StringIO import StringIO

TITLEFORMAT="%%TITLE%%"
WIKIQUOTEURL="http://en.wikiquote.org/w/api.php?format=json&action=query&titles=" + TITLEFORMAT + "&prop=revisions&rvprop=content"	

def preprocessTitle(title):
	""" For instance "Friedrich Nietzsche" would become "Friedrich_Nietzsche" """
	return title.replace(' ','%20')

def getURL(title):
	urlReadyTitle = preprocessTitle(title)
	urlForTitle = WIKIQUOTEURL.replace(TITLEFORMAT, urlReadyTitle)
	return urlForTitle

def downloadQuote(curler, title):
	buffer = StringIO()
	curler.setopt(curler.URL, getURL(title))
	curler.setopt(curler.WRITEDATA, buffer)
	curler.perform()
	return buffer.getvalue()

def main():
	curler = pycurl.Curl()
	body = downloadQuote(curler, "Friedrich Nietzsche")
	jsonObject = json.loads(body)
	for key in jsonObject.iterkeys():
		print key
	curler.close()

if __name__ == '__main__':
	main()