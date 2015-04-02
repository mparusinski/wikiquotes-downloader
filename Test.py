# coding=UTF-8
import unittest
import os
import sys
import re
import copy
import pycurl
import StringIO

from WikiquotesRetriever import *
from InternalRepresentation import *
from CleanIR import *
from DetectLanguage import *

REBUILD_BASELINES = False

def safer_system_call(call):
    print "---------------------------------------------------------------------"
    print "The following command is to be executed"
    print "\t" + call
    valid_response = False
    while not valid_response:
        user_response = raw_input("Do you wish to execute this command? (YES/NO) ")
        if user_response == "YES":
            valid_response = True
            os.system(call)
        elif user_response == "NO":
            valid_response = True
        else:
            print "Please type YES or NO!"

class TestDetectLanguage(unittest.TestCase):

    def test_find_english_sentence(self):
        language_detector = LanguageDetector()
        english_score = language_detector.score_language("English", \
            "Once upon a time there was a sausage called Baldrick")
        french_score = language_detector.score_language("English", \
            "Il etait une fois une saucisse nomme Baldrick")
        self.assertTrue(english_score > french_score)

    def test_detect_english(self):
        language_detector = LanguageDetector()
        language = language_detector.detect_language(\
            "Once upon a time there was a sausage called Baldrick")
        self.assertTrue(language == "English")

    def test_detect_german(self):
        language_detector = LanguageDetector()
        language = language_detector.detect_language(\
            "Man verdirbt einen Jüngling am sichersten, wenn man ihn anleitet,"\
            " den Gleichdenkenden höher zu achten, als den Andersdenkenden.")
        self.assertTrue(language == "German")


class BaselineBuilder(object):

    def __init__(self):
        pass


def run_baselines_builders():
    regex = re.compile('^rebuild')
    subclasses_list = BaselineBuilder.__subclasses__()
    for subclass in subclasses_list:
        subclass_name = subclass.__name__
        obj = globals()[subclass_name]()
        methods = [method for method in dir(subclass) if callable(getattr(obj, method))]
        for method in methods:
            if regex.match(method):
                eval(subclass_name + '().' + method + '()')


class IRTransformationsBaselines(BaselineBuilder):

    def rebuild_test_correct_disputed_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_disputed.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_disputed(wikitext_ir)
            with open(baseline_file, 'w') as writehandle:
                writehandle.write(wikitext_ir.__str__())

    def rebuild_test_correct_misattributed_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_misattributed.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_misattributed(wikitext_ir)
            with open(baseline_file, 'w') as writehandle:
                writehandle.write(wikitext_ir.__str__())

    def rebuild_test_correct_quote_about_x_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_quotes_about_x.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_quotes_about_x(wikitext_ir)
            with open(baseline_file, 'w') as writehandle:
                writehandle.write(wikitext_ir.__str__())

    def rebuild_test_correct_noise_section_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_noise_sections.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_noise_sections(wikitext_ir)
            with open(baseline_file, 'w') as writehandle:
                writehandle.write(wikitext_ir.__str__())


class IRTransformationsTest(unittest.TestCase):

    def test_correct_disputed_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_disputed.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_disputed(wikitext_ir)
            with open(baseline_file, 'r') as baseline_file_handle:
                baseline = baseline_file_handle.read()
                self.assertTrue(baseline == wikitext_ir.__str__())

    def test_correct_misattributed_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_misattributed.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_misattributed(wikitext_ir)
            with open(baseline_file, 'r') as baseline_file_handle:
                baseline = baseline_file_handle.read()
                self.assertTrue(baseline == wikitext_ir.__str__())

    def test_correct_quote_about_x_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_quotes_about_x.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_quotes_about_x(wikitext_ir)
            with open(baseline_file, 'r') as baseline_file_handle:
                baseline = baseline_file_handle.read()
                self.assertTrue(baseline == wikitext_ir.__str__())

    def test_correct_noise_section_removal(self):
        baseline_file = 'baselines/Friedrich_Nietzsche_no_noise_sections.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            remove_noise_sections(wikitext_ir)
            with open(baseline_file, 'r') as baseline_file_handle:
                baseline = baseline_file_handle.read()
                self.assertTrue(baseline == wikitext_ir.__str__())

    def test_removers_commute(self):
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir_left = ir_from_json(external_json_content)
            wikitext_ir_right = copy.deepcopy(wikitext_ir_left)
            remove_misattributed(wikitext_ir_left)
            remove_disputed(wikitext_ir_left)
            remove_disputed(wikitext_ir_right)
            remove_misattributed(wikitext_ir_right)
            self.assertTrue(\
                wikitext_ir_left.__str__() == wikitext_ir_right.__str__())


class WikitextIRBaselines(BaselineBuilder):

    def rebuild_test_correct_wikitext_ir(self):
        baseline_file = 'baselines/Friedrich_Nietzsche.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            with open(baseline_file, 'w') as writehandle:
                writehandle.write(wikitext_ir.__str__())


class WikitextIRTest(unittest.TestCase):

    def test_correct_wikitext_ir(self):
        baseline_file = 'baselines/Friedrich_Nietzsche.wikitextIR'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            wikitext_ir = ir_from_json(external_json_content)
            with open(baseline_file, 'r') as baseline_file_handle:
                baseline_ir = baseline_file_handle.read()
                self.assertTrue(baseline_ir == wikitext_ir.__str__())


class WikitextExtractorBaselines(BaselineBuilder):

    def rebuild_test_correct_wikitext_built(self):
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            title, wikitext_content = wikitext_from_json(external_json_content)
            with open('baselines/Friedrich_Nietzsche.wikitext', 'w') as writehandle:
                writehandle.write(wikitext_content.encode('UTF-8'))


class WikitextExtractorTest(unittest.TestCase):

    def test_correct_wikitext_build(self):
        baseline_file = 'baselines/Friedrich_Nietzsche.wikitext'
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
            title, wikitext_content = wikitext_from_json(external_json_content)
            with open(baseline_file, 'r') as readhandle:
                wikitextbaseline = readhandle.read()
                self.assertTrue(wikitext_content.encode('UTF-8') == wikitextbaseline)

    def test_other_wikitext_build(self):
        wiki_retriever = WikiquotesRetriever()
        wiki_retriever.setup_networking()
        online_json_content = wiki_retriever.download_quote("Baruch Spinoza")
        wiki_retriever.close_networking()
        title, wikitext_content = wikitext_from_json(online_json_content)

    def test_empty_wikitext(self):
        with self.assertRaises(InvalidWikitext):
            title, wikitext = wikitext_from_json("")


class WikiquotesRetrieverBaselines(BaselineBuilder):
    """Class to rebuild baselines"""

    def rebuild_test_correct_json_downloaded(self):
        quoteURL = "\"http://en.wikiquote.org/w/api.php?format=json&action=query&titles=Friedrich%20Nietzsche&prop=revisions&rvprop=content\""
        safer_system_call('curl ' + quoteURL + ' > baselines/Friedrich_Nietzsche.json')


class WikiquotesRetrieverTest(unittest.TestCase):

    def test_downloading_various(self):
        wiki_retriever = WikiquotesRetriever()
        wiki_retriever.setup_networking()
        wiki_retriever.download_quote("Friedrich_Nietzsche")
        wiki_retriever.download_quote("Baruch Spinoza")
        wiki_retriever.close_networking()

    def test_correct_json_downloaded(self):
        wiki_retriever = WikiquotesRetriever()
        wiki_retriever.setup_networking()
        online_json_content = wiki_retriever.download_quote("Friedrich Nietzsche")
        wiki_retriever.close_networking()
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
        self.assertTrue(external_json_content == online_json_content)

    def test_not_hardcoded_json_downloaded(self):
        wiki_retriever = WikiquotesRetriever()
        wiki_retriever.setup_networking()
        online_json_content = wiki_retriever.download_quote("Plato")
        wiki_retriever.close_networking()
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
        self.assertTrue(not external_json_content == online_json_content)

    def test_non_fn_title(self):
        try:
            wiki_retriever = WikiquotesRetriever()
            wiki_retriever.setup_networking()
            online_json_content = wiki_retriever.download_quote("Baruch Spinoza")
            wiki_retriever.close_networking()
        except:
            self.fail("No exception should be thrown")

    def test_invalid_title(self):
        with self.assertRaises(InvalidTitleException):
            wiki_retriever = WikiquotesRetriever()
            wiki_retriever.setup_networking()
            online_json_content = wiki_retriever.download_quote("SpinozaBanana")
            wiki_retriever.close_networking()


def rebuild_baselines():
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!!!! WARNING: Rebuilding baselines instead of running tests        !!!!"
    print "!!!! Execute at your own risk                                      !!!!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    run_baselines_builders()

def main():
    wikiquote_url = "http://en.wikiquote.org"
    try:
        curler = pycurl.Curl()
        buffer_string = StringIO()
        curler.setopt(curler.URL, wikiquote_url)
        curler.setopt(curler.WRITEDATA, buffer_string)
        curler.perform()
        curler.close()
        if REBUILD_BASELINES:
            rebuild_baselines()
        else:
            unittest.main()
    except pycurl.error:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "!!!! ERROR: Unable to get Curl to connect wikiquote main page. !!!!"
        print "!!!! A connection to wikiquote is required to run the tests    !!!!"
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

if __name__ == "__main__":
    main()
