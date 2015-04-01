# coding=UTF-8
import re
from IRBuilder import WikitextIR
from DetectLanguage import LanguageDetector

def remove_misattributed(wikitext_ir):
    misattributed_regex = re.compile('== Misattributed ==')
    root_node = wikitext_ir.get_root()
    root_node.remove_children_using_regex(misattributed_regex)

def remove_disputed(wikitext_ir):
    disputed_regex = re.compile('== Disputed ==')
    root_node = wikitext_ir.get_root()
    root_node.remove_children_using_regex(disputed_regex)

def remove_quotes_about_x(wikitext_ir):
    about_x_regex = re.compile(r'== Quotes about [a-zA-Z\s]+ ==')
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
    quotes_regex = re.compile('(== Quotes ==)|(== Quotations ==)')
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
    sections_regex = re.compile(r'== [a-zA-Z0-9\s]+ ==')
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

def remove_html(wikitext_ir):
    html_regex = re.compile(r'<[/]?[\w]+>')
    def remove_html_helper(node):
        string = node.get_string()
        new_string = html_regex.sub('', string)
        node.set_string(new_string)
    root_node = wikitext_ir.get_root()
    root_node.do_for_all_ancestry(remove_html_helper)

def clean_string_with_regexes(string, regex_sub_list):
    new_string = string
    for regex, sub_str in regex_sub_list:
        new_string = regex.sub(sub_str, new_string)
    return new_string

def markup_cleaner(wikitext_ir):
    regex_sub_list = []
    regex_sub_list.append((re.compile(r'\'\'\''), r''))
    regex_sub_list.append((re.compile(r'\'\''), r''))
    regex_sub_list.append((re.compile(r'\[\[([\s\w:\.\\/]+\|)([\s\w]+)\]\]', re.UNICODE), r'\2'))
    regex_sub_list.append((re.compile(r'\[\[([\w\s]+)\]\]', re.UNICODE), r'\1'))
    regex_sub_list.append((re.compile(r'\[(.+)\]'), r''))
    def clean_markup_internal(node):
        string = node.get_string()
        clean_string = clean_string_with_regexes(string, regex_sub_list)
        node.set_string(clean_string)
    root_node = wikitext_ir.get_root()
    root_node.do_for_all_ancestry(clean_markup_internal)

def clean_ir(wikitext_ir):
    remove_sections(wikitext_ir)
    remove_second_depth(wikitext_ir)
    remove_leading_stars(wikitext_ir)
    remove_quote_delimiters(wikitext_ir)
    fix_internal_quotes(wikitext_ir)
    markup_cleaner(wikitext_ir)
    remove_html(wikitext_ir)

if __name__ == '__main__':
    pass
