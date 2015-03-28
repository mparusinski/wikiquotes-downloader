import pycurl
from StringIO import StringIO

PEEK_AHEAD_FOR_ERROR_LENGTH = 321

class InvalidTitleException(Exception):

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return repr(self.title)


class WikiquotesRetriever(object):
    """This class retrieves pages from Wikiquotes"""
    def __init__(self):
        self.title_place_holder   = "%%TITLE%%"
        self.wikiquote_url_format = "http://en.wikiquote.org/w/api.php?format=json&action=query&titles=" \
            + self.title_place_holder + "&prop=revisions&rvprop=content"
        self.curler = None

    def setup_networking(self):
        self.curler = pycurl.Curl()

    def close_networking(self):
        self.curler.close()

    def __preprocess_title(self, title):
        """ For instance "Friedrich Nietzsche" would become "Friedrich_Nietzsche" """
        return title.replace(' ','%20')

    def __getURL(self, title):
        url_ready_title = self.__preprocess_title(title)
        url_for_title = self.wikiquote_url_format.replace(self.title_place_holder, url_ready_title)
        return url_for_title

    def download_quote(self, title):
        buffer = StringIO()
        self.curler.setopt(self.curler.URL, self.__getURL(title))
        self.curler.setopt(self.curler.WRITEDATA, buffer)
        self.curler.perform()
        json_text = buffer.getvalue()
        peek_ahead = json_text[0:PEEK_AHEAD_FOR_ERROR_LENGTH]
        peek_text = "\"pages\":{\"-1\""
        if peek_text in peek_ahead:
            raise InvalidTitleException(title)
        return json_text

def main():
    wiki_retriever = WikiquotesRetriever()
    wiki_retriever.setup_networking()
    print wiki_retriever.download_quote("Friedrich Nietzsche")
    wiki_retriever.close_networking()

if __name__ == '__main__':
    main()
