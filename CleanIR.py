# coding=UTF-8
import re
from IRBuilder import *
from DetectLanguage import *

def remove_misattributed(wikitext_ir):
    misattributed_regex = re.compile('== Misattributed ==')
    root_node = wikitext_ir.get_root()
    root_node.remove_children_using_regex(misattributed_regex)

def remove_disputed(wikitext_ir):
    disputed_regex = re.compile('== Disputed ==')
    root_node = wikitext_ir.get_root()
    root_node.remove_children_using_regex(disputed_regex)

def remove_quotes_about_x(wikitext_ir):
    about_x_regex = re.compile('== Quotes about [a-zA-Z\s]+ ==')
    root_node = wikitext_ir.get_root()
    root_node.remove_children_using_regex(about_x_regex)

def remove_noise_sections(wikitext_ir):
    """Remove sections that have nothing to do with quotes"""
    noise_sections = re.compile('== See also ==')
    root_node = wikitext_ir.get_root()
    root_node.remove_children_using_regex(noise_sections)

def fix_translation(translated_node):
    children = translated_node.get_children()
    first_child = children[0]
    new_string = first_child.get_string()
    new_string = new_string[1:] # drop the first '*'
    translated_node.set_string(new_string)
    translated_node.remove_child(first_child)

def remove_translations(wikitext_ir):
    language_detector = LanguageDetector()
    def detect_translation(node):
        return not language_detector.detect_language(node.get_string()) == "English"
    root_node = wikitext_ir.get_root()
    quotes_regex = re.compile('== Quotes ==')
    quotes_subnodes = root_node.find_children_using_regex(quotes_regex)
    num_subnodes = len(quotes_subnodes)
    if num_subnodes > 1:
        raise InvalidWikitext("More than one \"QUOTES\" section is not supported")
    elif num_subnodes == 0:
        raise InvalidWikitext("No \"QUOTES\" section found. Please contact developer")
    else:
        quotes_node = quotes_subnodes[0]
        quotes_node.get_string()
        translated_nodes = quotes_node.find_children_using_function(detect_translation)
        for node_translated in translated_nodes:
            fix_translation(node_translated)

def remove_noise(wikitext_ir):
    remove_misattributed(wikitext_ir)
    remove_disputed(wikitext_ir)
    remove_quotes_about_x(wikitext_ir)
    remove_noise_sections(wikitext_ir)

def remove_sections(wikitext_ir):
    sections_regex= re.compile('== [a-zA-Z0-9\s]+ ==')
    root_node = wikitext_ir.get_root()
    root_node.remove_nodes_using_regex(sections_regex)

def remove_second_depth(wikitext_ir):
    root_node = wikitext_ir.get_root()
    children = root_node.get_children()
    for child in children:
        child.remove_children()

def remove_leading_stars(wikitext_ir):
    def cleaning_function(node):
        string = node.get_string()
        new_string = string.lstrip('* ')
        node.set_string(new_string)
    root_node = wikitext_ir.get_root()
    root_node.do_for_all_ancestry(cleaning_function)

def remove_quote_delimiters(wikitext_ir):
    def cleaning_function(node):
        string = node.get_string()
        new_string = string.lstrip("'")
        new_string = new_string.rstrip("'")
        node.set_string(new_string)
    root_node = wikitext_ir.get_root()
    root_node.do_for_all_ancestry(cleaning_function)

def fix_internal_quotes(wikitext_ir):
    double_quote_regex = re.compile(r'(\")')
    def fix_quote_helper(node):
        string = node.get_string()
        new_string = double_quote_regex.sub('\\\"', string)
        node.set_string(new_string)
    root_node = wikitext_ir.get_root()
    root_node.do_for_all_ancestry(fix_quote_helper)

def markup_cleaner(wikitext_ir):
    """
    Markup is completely removed and is unsupported for now
    """
    italic_regex = re.compile(r'\'\'')
    bold_regex = re.compile(r'\'\'\'')
    # TODO: Add support for escape wiki markup
    def clean_markup_internal(node):
        string = node.get_string()
        no_bold_string = bold_regex.sub('', string)
        no_italic_no_bold_string = italic_regex.sub('', no_bold_string)
        node.set_string(no_italic_no_bold_string)
    root_node = wikitext_ir.get_root()
    root_node.do_for_all_ancestry(clean_markup_internal)

def clean_ir(wikitext_ir):
    remove_sections(wikitext_ir)
    remove_second_depth(wikitext_ir)
    remove_leading_stars(wikitext_ir)
    remove_quote_delimiters(wikitext_ir)
    fix_internal_quotes(wikitext_ir)
    markup_cleaner(wikitext_ir)

def main():
    with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
        external_json_content = filehandle.read()
        wikitext = Wikitext(external_json_content)
        irinstance = WikitextIR(wikitext)
        remove_noise(irinstance)
        remove_translations(irinstance)
        clean_ir(irinstance)
        print irinstance.toString()

if __name__ == '__main__':
    main()
