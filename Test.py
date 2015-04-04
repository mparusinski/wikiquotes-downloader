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
NETWORKING = True
try:
    wikiquote_url = "http://en.wikiquote.org"
    curler = pycurl.Curl()
    buffer_string = StringIO()
    curler.setopt(curler.URL, wikiquote_url)
    curler.setopt(curler.WRITEDATA, buffer_string)
    curler.perform()
    curler.close()
except pycurl.error:
    NETWORKING = False

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

class TestIRNode(unittest.TestCase):

    def test_irnode_empty_value(self):
        emptynode = IRNode("")
        self.assertTrue(emptynode.value == "")
        self.assertTrue(emptynode.parent_node == None)
        self.assertTrue(len(emptynode.children) == 0)

    def test_adding_child_node(self):
        emptynode_1 = IRNode("")
        emptynode_2 = IRNode("")
        emptynode_1.add_child_node(emptynode_2)
        self.assertTrue(len(emptynode_1.children) == 1)
        self.assertTrue(len(emptynode_2.children) == 0)
        self.assertTrue(emptynode_1.children[0] == emptynode_2)
        self.assertTrue(emptynode_2.parent_node == emptynode_1)

    def test_adding_invalid_node(self):
        with self.assertRaises(InvalidIRNodeOperation):
            dummynode = IRNode("")
            dummynode.add_child_node(None)

    def test_adding_not_parentless_node(self):
        with self.assertRaises(InvalidIRNodeOperation):
            parent1 = IRNode("parent1")
            parent2 = IRNode("parent2")
            child = IRNode("child")
            parent1.add_child_node(child)
            parent2.add_child_node(child)

    def test_do_for_all_in_tree_simple(self):
        def dummy_function(node):
            node.value = "dummy"
        emptynode = IRNode("")
        emptynode.do_for_all_in_tree(dummy_function)
        self.assertTrue(emptynode.value == "dummy")
        self.assertTrue(len(emptynode.children) == 0)
        self.assertTrue(emptynode.parent_node == None)

    def test_do_for_all_in_tree_complex(self):
        def dummy_function(node):
            node.value = "dummy"
        emptynode = IRNode("")
        emptynode.add_child_node(IRNode(""))
        emptynode.do_for_all_in_tree(dummy_function)
        self.assertTrue(emptynode.value == "dummy")
        self.assertTrue(len(emptynode.children) == 1)
        self.assertTrue(emptynode.children[0].value == "dummy")
        self.assertTrue(len(emptynode.children[0].children) == 0)

    def test_str_function_simple(self):
        dummynode = IRNode("dummy")
        self.assertTrue(dummynode.__str__() == "dummy")

    def test_str_function_complex(self):
        dummynode = IRNode("dummy")
        dummynode.add_child_node(IRNode("dummy"))
        self.assertTrue(dummynode.__str__() == "dummy\n  dummy")

    def test_remove_children_single(self):
        singlenode = IRNode("")
        singlenode.remove_children()
        self.assertTrue(len(singlenode.children) == 0)

    def test_remove_children_single_child(self):
        singlechildparent = IRNode("")
        childnode = IRNode("")
        singlechildparent.add_child_node(childnode)
        singlechildparent.remove_children()
        self.assertTrue(len(singlechildparent.children) == 0)
        self.assertTrue(childnode.parent_node == None)

    def test_remove_children_nasty_case(self):
        anode = IRNode("")
        anode.add_child_node(anode)
        anode.remove_children()
        self.assertTrue(len(anode.children) == 0)

    def test_remove_child_no_children(self):
        anode = IRNode("")
        anode.remove_child(IRNode("dummy"))

    def test_remove_child_simple(self):
        aparent = IRNode("parent")
        achild = IRNode("child")
        aparent.add_child_node(achild)
        aparent.remove_child(achild)
        self.assertFalse(achild in aparent.children)
        self.assertTrue(achild.parent_node == None)

    def test_remove_child_with_grandparents(self):
        aparent = IRNode("parent")
        achild = IRNode("child")
        agrandchild = IRNode("grandchild")
        achild.add_child_node(agrandchild)
        aparent.add_child_node(achild)
        aparent.remove_child(achild)
        self.assertTrue(agrandchild.parent_node == achild)
        self.assertTrue(achild.parent_node == None)

    def test_remove_child_nochild(self):
        aparent = IRNode("parent")
        achild = IRNode("child")
        orphan = IRNode("orphan")
        aparent.add_child_node(achild)
        aparent.remove_child(orphan)
        self.assertTrue(len(aparent.children) == 1)
        self.assertTrue(aparent.children[0] == achild)
        self.assertTrue(achild.parent_node == aparent)

    def test_find_children_using_regex_no_childs(self):
        nochildnode = IRNode("nochildnode")
        foundchilds = nochildnode.find_children_using_regex(re.compile(r''))
        self.assertTrue(len(foundchilds) == 0)

    def test_find_children_using_regex_all_match(self):
        parent = IRNode("parent")
        num = 10
        for i in xrange(num):
            node = IRNode("child " + str(i))
            parent.add_child_node(node)
        all_regex = re.compile(r'child')
        foundchilds = parent.find_children_using_regex(all_regex)
        self.assertTrue(len(foundchilds) == num)

    def test_find_children_using_regex_only_one_match(self):
        parent = IRNode("parent")
        matchchild = IRNode("match")
        otherchild = IRNode("other")
        parent.add_child_node(matchchild)
        parent.add_child_node(otherchild)
        match_regex = re.compile(r'match')
        foundchilds = parent.find_children_using_regex(match_regex)
        self.assertTrue(len(parent.children) == 2)
        self.assertTrue(len(foundchilds) == 1)
        self.assertTrue(foundchilds[0] == matchchild)

    def test_find_children_using_function_no_childs(self):
        def dummy_function(node):
            return True
        nochildnode = IRNode("nochildnode")
        foundchilds = nochildnode.find_children_using_function(dummy_function)
        self.assertTrue(len(foundchilds) == 0)

    def test_find_children_using_function_all_match(self):
        parent = IRNode("parent")
        num = 10
        for i in xrange(num):
            node = IRNode("child " + str(i))
            parent.add_child_node(node)
        def dummy_function(node):
            return True
        foundchilds = parent.find_children_using_function(dummy_function)
        self.assertTrue(len(foundchilds) == num)

    def test_find_children_using_function_no_match(self):
        parent = IRNode("parent")
        num = 10
        for i in xrange(num):
            node = IRNode("child " + str(i))
            parent.add_child_node(node)
        def dummy_function(node):
            return False
        foundchilds = parent.find_children_using_function(dummy_function)
        self.assertTrue(len(foundchilds) == 0)

    def test_find_children_using_simple_function(self):
        parent = IRNode("parent")
        num = 10
        for i in xrange(num):
            node = IRNode(str(i))
            parent.add_child_node(node)
        def dummy_function(node):
            return int(node.value) % 2 == 0
        foundchilds = parent.find_children_using_function(dummy_function)
        self.assertTrue(len(foundchilds) == (num / 2))

    def test_remove_children_using_regex_no_childs(self):
        nochildnode = IRNode("nochildnode")
        nochildnode.remove_children_using_regex(re.compile(r''))
        self.assertTrue(len(nochildnode.children) == 0)

    def test_remove_children_using_regex_all_match(self):
        parent = IRNode("parent")
        num = 10
        for i in xrange(num):
            node = IRNode("child " + str(i))
            parent.add_child_node(node)
        all_regex = re.compile(r'child')
        parent.remove_children_using_regex(all_regex)
        self.assertTrue(len(parent.children) == 0)

    def test_remove_children_using_regex_only_one_match(self):
        parent = IRNode("parent")
        matchchild = IRNode("match")
        otherchild = IRNode("other")
        parent.add_child_node(matchchild)
        parent.add_child_node(otherchild)
        match_regex = re.compile(r'match')
        parent.remove_children_using_regex(match_regex)
        self.assertTrue(len(parent.children) == 1)
        self.assertTrue(parent.children[0] == otherchild)
        self.assertTrue(matchchild.parent_node == None)

    def test_remove_node_empty(self):
        emptynode = IRNode("empty")
        emptynode.remove_node(IRNode(""))
        self.assertTrue(len(emptynode.children) == 0)

    def test_remove_node_one_childless_child(self):
        parent = IRNode("parent")
        child = IRNode("child")
        parent.add_child_node(child)
        parent.remove_node(child)
        self.assertTrue(len(parent.children) == 0)
        self.assertTrue(child.parent_node == None)

    def test_remove_node_childbearingchild_child(self):
        parent = IRNode("parent")
        child = IRNode("child")
        grandchild = IRNode("grandchild")
        parent.add_child_node(child)
        child.add_child_node(grandchild)
        parent.remove_node(child)
        self.assertTrue(len(parent.children) == 1)
        self.assertTrue(parent.children[0] == grandchild)
        self.assertTrue(len(child.children) == 0)
        self.assertTrue(child.parent_node == None)
        self.assertTrue(grandchild.parent_node == parent)

    def test_remove_node_multiple_descendants(self):
        parent = IRNode("parent")
        child1 = IRNode("child1")
        child2 = IRNode("child2")
        grandchild11 = IRNode("grandchild11")
        grandchild12 = IRNode("grandchild12")
        grandchild21 = IRNode("grandchild21")
        grandchild22 = IRNode("grandchild22")
        parent.add_child_node(child1)
        parent.add_child_node(child2)
        child1.add_child_node(grandchild11)
        child1.add_child_node(grandchild12)
        child2.add_child_node(grandchild21)
        child2.add_child_node(grandchild22)
        parent.remove_node(child2)
        self.assertTrue(len(parent.children) == 3)
        self.assertTrue(child1.parent_node == parent)
        self.assertTrue(grandchild21.parent_node == parent)
        self.assertTrue(grandchild22 in parent.children)
        self.assertTrue(len(child1.children) == 2)
        parent.remove_node(child1)
        self.assertTrue(len(parent.children) == 4)
        self.assertTrue(child1.parent_node == None)
        self.assertTrue(grandchild21.parent_node == parent)
        self.assertTrue(grandchild22 in parent.children)
        self.assertTrue(len(child1.children) == 0)

    def test_remove_nodes_using_regex_no_childs(self):
        singlenode = IRNode("singlenode")
        singlenode.remove_nodes_using_regex(re.compile(r''))
        self.assertTrue(len(singlenode.children) == 0)

    def test_remove_nodes_using_regex_all_match(self):
        parent = IRNode("parent")
        child1 = IRNode("child1")
        child2 = IRNode("child2")
        parent.add_child_node(child1)
        parent.add_child_node(child2)
        parent.remove_nodes_using_regex(re.compile(r''))
        self.assertTrue(len(parent.children) == 0)
        self.assertTrue(child1.parent_node == None)
        self.assertTrue(child2.parent_node == None)

    def test_remove_nodes_using_regex_one_match(self):
        parent = IRNode("parent")
        child1 = IRNode("child1")
        child2 = IRNode("child2")
        parent.add_child_node(child1)
        parent.add_child_node(child2)
        child1.add_child_node(IRNode(""))
        child2.add_child_node(IRNode(""))
        parent.remove_nodes_using_regex(re.compile(r'child2'))
        self.assertTrue(len(parent.children) == 2)
        self.assertTrue(parent.children[0] == child1)
        self.assertFalse(parent.children[1] == child2)
        self.assertTrue(child2.parent_node == None)


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

    @unittest.skipIf(not NETWORKING,
                     "not able to establish a connection to wikiquote.org")
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

    @unittest.skipIf(not NETWORKING,
                     "not able to establish a connection to wikiquote.org")
    def test_downloading_various(self):
        wiki_retriever = WikiquotesRetriever()
        wiki_retriever.setup_networking()
        wiki_retriever.download_quote("Friedrich_Nietzsche")
        wiki_retriever.download_quote("Baruch Spinoza")
        wiki_retriever.close_networking()

    @unittest.skipIf(not NETWORKING,
                     "not able to establish a connection to wikiquote.org")
    def test_correct_json_downloaded(self):
        wiki_retriever = WikiquotesRetriever()
        wiki_retriever.setup_networking()
        online_json_content = wiki_retriever.download_quote("Friedrich Nietzsche")
        wiki_retriever.close_networking()
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
        self.assertTrue(external_json_content == online_json_content)

    @unittest.skipIf(not NETWORKING,
                     "not able to establish a connection to wikiquote.org")
    def test_not_hardcoded_json_downloaded(self):
        wiki_retriever = WikiquotesRetriever()
        wiki_retriever.setup_networking()
        online_json_content = wiki_retriever.download_quote("Plato")
        wiki_retriever.close_networking()
        with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
            external_json_content = filehandle.read()
        self.assertTrue(not external_json_content == online_json_content)

    @unittest.skipIf(not NETWORKING,
                     "not able to establish a connection to wikiquote.org")
    def test_non_fn_title(self):
        try:
            wiki_retriever = WikiquotesRetriever()
            wiki_retriever.setup_networking()
            online_json_content = wiki_retriever.download_quote("Baruch Spinoza")
            wiki_retriever.close_networking()
        except:
            self.fail("No exception should be thrown")

    @unittest.skipIf(not NETWORKING,
                     "not able to establish a connection to wikiquote.org")
    def test_invalid_title(self):
        with self.assertRaises(InvalidTitleException):
            wiki_retriever = WikiquotesRetriever()
            wiki_retriever.setup_networking()
            online_json_content = wiki_retriever.download_quote("SpinozaBanana")
            wiki_retriever.close_networking()


def rebuild_baselines():
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!!!! WARNING: Rebuilding baselines instead of running tests      !!!!"
    print "!!!! Execute at your own risk                                    !!!!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    run_baselines_builders()

def main():
    wikiquote_url = "http://en.wikiquote.org"
    if REBUILD_BASELINES:
        if NETWORKING:
            rebuild_baselines()
        else:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print "!!!! ERROR: No connection to wikiquote main page                 !!!!"
            print "!!!! (Re)building baselines requires a working connection        !!!!"
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    else:
        if not NETWORKING:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print "!!!! WARNING: Unable to get Curl to connect wikiquote main page. !!!!"
            print "!!!! A connection to wikiquote is required to run some tests     !!!!"
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        unittest.main()
        
if __name__ == "__main__":
    main()
