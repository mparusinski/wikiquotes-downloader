# coding=UTF-8
import json
import re
from StringIO import StringIO

def inspect_json_object(json):
    for key in json.iterkeys():
        string_object_value = unicode(json[key])
        print key + ": " + string_object_value[0:100]

def inspect_json_list(json):
    for elem in json:
        string_elem = unicode(elem)
        print string_elem[0:100]

class WikitextIRNode(object):
    """Defines a node in the internal representation of a wikitext page"""
    def __init__(self, current_string, parent_node = None):
        self.current_string = current_string
        self.children = []
        self.parent_node = parent_node

    def add_child(self, wikitext_ir_node):
        self.children.append(wikitext_ir_node)

    def set_string(self, new_string):
        self.current_string = new_string

    def get_parent(self):
        return self.parent_node

    def get_children(self):
        return self.children

    def get_string(self):
        return self.current_string

    def to_string_list(self, tabulation):
        """Build a list of strings"""
        first_item = tabulation + self.current_string
        accum = [first_item]
        for child in self.children:
            child_string_list = child.to_string_list(tabulation + "  ")
            accum = accum + child_string_list
        return accum

    def to_string(self):
        string_list = self.to_string_list("")
        return "\n".join(string_list)

    def do_for_all_ancestry(self, function):
        for child in self.children:
            function(child)
            child.do_for_all_ancestry(function)

    def find_children_using_regex(self, regex):
        # assuming regex is precompiled
        found_list = []
        for child in self.children:
            if regex.match(child.get_string()):
                found_list.append(child)
        return found_list

    def find_children_using_function(self, function):
        found_list = []
        for child in self.children:
            if function(child):
                found_list.append(child)
        return found_list

    def remove_children(self):
        self.children = []

    def remove_children_using_regex(self, regex):
        children_list_copy = list(self.children) # copy, but not deepcopy
        for child in children_list_copy:
            if regex.match(child.get_string()):
                self.children.remove(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_nodes_using_regex(self, regex):
        children_list_copy = list(self.children)
        for child in children_list_copy:
            if regex.match(child.get_string()):
                self.remove_child_node(child)

    def remove_child_node(self, node):
        # surgically remove node but not its children
        nodes_children = node.get_children()
        for node_child in nodes_children:
            node_child.parentNode = self
        nodes_index = self.children.index(node)
        new_children = []
        for child in self.children:
            if child == node:
                new_children = new_children + nodes_children
            else:
                new_children.append(child)
        self.children = new_children


class WikitextIR:
    """Defines an internal representation of a wikitext page"""
    def __init__(self, wikitext):
        self.root_node = WikitextIRNode(wikitext.get_wikitext_title())
        self.__parse_text(wikitext.get_wikitext_string())

    def __parse_text(self, text_to_parse):
        current_node = self.root_node
        current_depth = 0
        for line in text_to_parse.splitlines():
            if self.__valid_line(line):
                depth = self.__find_depth(line)
                if depth > current_depth: # Going deeper
                    if not (depth - current_depth == 1):
                        # TODO Raise appropriate error
                        print "Parse error! Line " + line + " is not invalid"
                    else:
                        new_node = WikitextIRNode(line, parent_node=current_node)
                        current_node.add_child(new_node)
                        current_node = new_node
                        current_depth = depth
                else:
                    drop_amount = current_depth - depth
                    for i in xrange(drop_amount):
                        current_node = current_node.get_parent()
                    parent_node = current_node.get_parent()
                    new_node = WikitextIRNode(line, parent_node=parent_node)
                    parent_node.add_child(new_node)
                    current_node = new_node
                    current_depth = depth

    def __valid_line(self, line):
        return line.startswith("== ") or (len(line) > 0 and line[0] == '*')

    def __find_depth(self, line):
        if line.startswith("== "):
            return 1
        else:
            for idx, char in enumerate(line):
                if not char == '*':
                    return idx + 1
        return -1

    def get_root(self):
        return self.root_node

    def to_string(self):
        stringList = self.root_node.to_string_list("")
        string_none_formatted = "\n".join(stringList)
        return string_none_formatted.encode('UTF-8')


class InvalidWikitext(Exception):

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return repr(self.description)

class Wikitext(object):
    """Wikitext that is embedded in a jsonString"""
    def __init__(self, json_string):
        self.nodes = []
        self.key_string = "query.pages"
        self.page_title = None
        self.wikitext = None
        self.__extract_wikitext(json_string)

    def __process_page(self, page):
        page_keys = page.keys()
        page_id = page_keys[0]
        page_internal = page[page_id]
        self.page_title = page_internal['title']
        page_content = page_internal['revisions']
        page_element = page_content[0]
        self.wikitext = page_element["*"]

    def __extract_wikitext(self, json_string):
        try:
            json_content = json.loads(json_string)
            page = self.__get_address_json(json_content, self.key_string)
            self.__process_page(page)
        except ValueError:
            raise InvalidWikitext("Not a valid JSON file")

    def __get_address_json(self, json, address_string):
        tokens = address_string.split('.')
        json_content = json
        for token in tokens:
            json_content = json_content[token]
        return json_content

    def get_wikitext_string(self):
        return self.wikitext

    def get_wikitext_title(self):
        return self.page_title

def main():
    with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
        external_json_content = filehandle.read()
        wikitext = Wikitext(external_json_content)
        irinstance = WikitextIR(wikitext)
        print irinstance.to_string()

if __name__ == "__main__":
    main()
        