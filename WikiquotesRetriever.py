import pycurl
from StringIO import StringIO

PEEK_AHEAD_FOR_ERROR_LENGTH = 321
WIKIQUOTE_URL_BASE = "http://en.wikiquote.org/w/api.php?format=json&action=query&titles="

class InvalidTitleException(Exception):

    def __init__(self, title):
        super(InvalidTitleException, self).__init__(title)
        self.title = title

    def __str__(self):
        return repr(self.title)


class NetworkingException(Exception):

    def __init__(self, description):
        super(NetworkingException, self).__init__(description)
        self.description = description

    def __str__(self):
        return repr(self.description)


class WikiquotesRetriever(object):
    """This class retrieves pages from Wikiquotes"""
    def __init__(self):
        self.title_place_holder = "%%TITLE%%"
        self.wikiquote_url = WIKIQUOTE_URL_BASE + self.title_place_holder \
            + "&prop=revisions&rvprop=content"
        self.curler = None

    def setup_networking(self):
        self.curler = pycurl.Curl()

    def close_networking(self):
        self.curler.close()

    def __get_url(self, title):
        url_ready_title = title.replace(' ', '%20')
        url_for_title = self.wikiquote_url.replace(self.title_place_holder, url_ready_title)
        return url_for_title

    def download_quote(self, title):
        try:
            buffer_string = StringIO()
            self.curler.setopt(self.curler.URL, self.__get_url(title))
            self.curler.setopt(self.curler.WRITEDATA, buffer_string)
            self.curler.perform()
            json_text = buffer_string.getvalue()
            peek_ahead = json_text[0:PEEK_AHEAD_FOR_ERROR_LENGTH]
            peek_text = "\"pages\":{\"-1\""
            if peek_text in peek_ahead:
                raise InvalidTitleException(title)
            return json_text
        except pycurl.error:
            raise NetworkingException("Unable to connect to wikiquotes!")


if __name__ == '__main__':
    pass
