# coding=UTF-8
import re
from InternalRepresentation import InternalRepresentation, ir_from_json, InvalidWikitext
from DetectLanguage import LanguageDetector

def remove_misattributed(wikitext_ir):
    misattributed_regex = re.compile(r'==(\s)*((Misattributed)|(Attributed)|(Posthumous attributions))(\s)*==', re.IGNORECASE)
    root_node = wikitext_ir.root_node
    root_node.remove_children_using_regex(misattributed_regex)

def remove_disputed(wikitext_ir):
    disputed_regex = re.compile(r'==(\s)*Disputed(\s)*==')
    root_node = wikitext_ir.root_node
    root_node.remove_children_using_regex(disputed_regex)

def remove_quotes_about_x(wikitext_ir):
    about_x_regex = re.compile(r'==(\s)*(((Quotes)|(Quotations))\s)?((about)|(regarding))[\s]?[0-9a-zA-Z\s\.]*==', re.IGNORECASE)
    root_node = wikitext_ir.root_node
    root_node.remove_children_using_regex(about_x_regex)

def remove_noise_sections(wikitext_ir):
    """Remove sections that have nothing to do with quotes"""
    noise_sections = re.compile(r'==(\s)*((See also)|(External links)|(Sources)|(Also see)|(Primary sources))(\s)*==', re.IGNORECASE)
    root_node = wikitext_ir.root_node
    root_node.remove_children_using_regex(noise_sections)

def fix_translation(translated_node):
    children = translated_node.children
    if len(children) >= 1:
        first_child = children[0]
         # drop the first '*'
        translated_node.value = first_child.value[1:]
        translated_node.remove_child(first_child)
    else:
        print "WARNING: No translations for line \"" + translated_node.value + "\""
        translated_node.parent_node.remove_child(translated_node)

def remove_translations(wikitext_ir):
    language_detector = LanguageDetector()
    def detect_translation(node):
        return not language_detector.detect_language(node.value) == "English"
    root_node = wikitext_ir.root_node
    quotes_regex = re.compile(r'==(\s)*((Quotes)|(Quotations)|(Sourced)|(Quoted))(\s)*==')
    quotes_subnodes = root_node.find_children_using_regex(quotes_regex)
    num_subnodes = len(quotes_subnodes)
    title = root_node.value
    if num_subnodes > 1:
        raise InvalidWikitext("Page " + title + " more than one \"QUOTES\" section which is not supported")
    elif num_subnodes == 0:
        raise InvalidWikitext("No \"QUOTES\" section found in page " + title + ". Please contact developer")
    else:
        quotes_node = quotes_subnodes[0]
        quotes_node.value
        translated_nodes = quotes_node.find_children_using_function(detect_translation)
        for node_translated in translated_nodes:
            fix_translation(node_translated)

def remove_noise(wikitext_ir):
    remove_misattributed(wikitext_ir)
    remove_disputed(wikitext_ir)
    remove_quotes_about_x(wikitext_ir)
    remove_noise_sections(wikitext_ir)

def remove_sections(wikitext_ir):
    sections_regex = re.compile(r'==(\s)*[a-zA-Z0-9\s]+(\s)*==')
    root_node = wikitext_ir.root_node
    root_node.remove_nodes_using_regex(sections_regex)

def remove_second_depth(wikitext_ir):
    root_node = wikitext_ir.root_node
    children = root_node.children
    for child in children:
        child.remove_children()

def remove_leading_stars(wikitext_ir):
    def cleaning_function(node):
        node.value = node.value.lstrip('* ')
    root_node = wikitext_ir.root_node
    root_node.do_for_all_in_tree(cleaning_function)

def remove_quote_delimiters(wikitext_ir):
    def cleaning_function(node):
        node.value = node.value.lstrip("'").rstrip("'")
    root_node = wikitext_ir.root_node
    root_node.do_for_all_in_tree(cleaning_function)

def fix_internal_quotes(wikitext_ir):
    # This was not necessary
    double_quote_regex = re.compile(r'(\")')
    def fix_quote_helper(node):
        node.value = double_quote_regex.sub('\\\"', node.value)
    root_node = wikitext_ir.root_node
    root_node.do_for_all_in_tree(fix_quote_helper)

def replace_html_breaks(wikitext_ir):
    breakline_regex = re.compile(r'((<br[\s]*>)|(<br[\s]*/>))')
    def replace_html_helper(node):
        node.value = breakline_regex.sub('\n', node.value)
    root_node = wikitext_ir.root_node
    root_node.do_for_all_in_tree(replace_html_helper)

def remove_html(wikitext_ir):
    html_regex = re.compile(r'<(([/]?)|(![-]+))[\s\w#&\?\.\-:=\\\"\/]*(([/]?)|([-]*))>', re.UNICODE)
    def remove_html_helper(node):
        node.value = html_regex.sub(r'', node.value)
    root_node = wikitext_ir.root_node
    root_node.do_for_all_in_tree(remove_html_helper)

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
    regex_sub_list.append((re.compile(r'\{{1,2}[\s\w\.:\\\/]*\}{1,2}', re.UNICODE), r''))
    def clean_markup_internal(node):
        node.value = clean_string_with_regexes(node.value, regex_sub_list)
    root_node = wikitext_ir.root_node
    root_node.do_for_all_in_tree(clean_markup_internal)

def clean_ir(wikitext_ir):
    remove_sections(wikitext_ir)
    remove_second_depth(wikitext_ir)
    remove_leading_stars(wikitext_ir)
    remove_quote_delimiters(wikitext_ir)
    markup_cleaner(wikitext_ir)
    replace_html_breaks(wikitext_ir)
    remove_html(wikitext_ir)

if __name__ == '__main__':
    pass
