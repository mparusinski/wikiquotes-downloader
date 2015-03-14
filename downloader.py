import pycurl
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

def main():
	buffer = StringIO()
	curler = pycurl.Curl()
	curler.setopt(curler.URL, getURL("Friedrich Nietzsche"))
	curler.setopt(curler.WRITEDATA, buffer)
	curler.perform()
	curler.close()
	body = buffer.getvalue()
	print(body)

if __name__ == '__main__':
	main()