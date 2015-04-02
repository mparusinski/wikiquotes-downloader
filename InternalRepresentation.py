# coding=UTF-8
import json

def inspect_json(json_obj):
    for key in json_obj.iterkeys():
        string_object_value = unicode(json_obj[key])
        print key + ": " + string_object_value[0:100]

def json_elem_at(json_obj, address):
    tokens = address.split('.')
    json_content = json_obj
    for token in tokens:
        json_content = json_content[token]
    return json_content

class IRNode(object):
    """Defines a node in the internal representation of a wikitext page"""
    def __init__(self, value, parent_node=None):
        self.value = value
        self.children = []
        self.parent_node = parent_node

    def __eq__(self, other):
        if self.value == other.value and \
            len(self.children) == len(other.children):
            for (left_child, right_child) in \
                zip(self.children, other.children):
                if not left_child == right_child:
                    return False
            return True
        else:
            return False

    def add_child_node(self, ir_node):
        self.children.append(ir_node)
        ir_node.parent_node = self

    def to_string_list(self, tabulation):
        """Build a list of strings"""
        first_item = tabulation + self.value
        accum = [first_item]
        for child in self.children:
            child_string_list = child.to_string_list(tabulation + "  ")
            accum = accum + child_string_list
        return accum

    def __str__(self):
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
            if regex.match(child.value):
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
            if regex.match(child.value):
                self.children.remove(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_nodes_using_regex(self, regex):
        children_list_copy = list(self.children)
        for child in children_list_copy:
            if regex.match(child.value):
                self.remove_child_node(child)

    def remove_child_node(self, node):
        # surgically remove node but not its children
        nodes_children = node.children
        for node_child in nodes_children:
            node_child.parentNode = self
        new_children = []
        for child in self.children:
            if child == node:
                new_children = new_children + nodes_children
            else:
                new_children.append(child)
        self.children = new_children


class InternalRepresentation(object):
    """Defines an internal representation of a wikitext page"""
    def __init__(self, wikitext):
        title, wikitext_content = wikitext
        self.root_node = IRNode(title)
        self.__parse_text(wikitext_content)

    def __eq__(self, other):
        return self.root_node == other.root_node

    def __parse_text(self, text_to_parse):
        current_node = self.root_node
        current_depth = 0
        for line in text_to_parse.splitlines():
            if line.startswith("== ") or line.startswith("*"):
                current_node, current_depth = \
                    self.__parse_text_line(line, current_node, current_depth)

    def __parse_text_line(self, line, current_node, current_depth):
        depth = self.__find_depth(line)
        if depth > current_depth: # Going deeper
            if not depth - current_depth == 1:
                raise InvalidWikitext("\"" + line + "\" is not valid!"\
                    " Can't be parsed")
            else:
                new_node = IRNode(line, parent_node=current_node)
                current_node.add_child_node(new_node)
                current_node = new_node
                current_depth = depth
        else:
            drop_amount = current_depth - depth
            for i in xrange(drop_amount):
                current_node = current_node.parent_node
            curr_parent_node = current_node.parent_node
            new_node = IRNode(line, parent_node=curr_parent_node)
            curr_parent_node.add_child_node(new_node)
            current_node = new_node
            current_depth = depth
        return current_node, current_depth

    def __find_depth(self, line):
        if line.startswith("== "):
            return 1
        else:
            for idx, char in enumerate(line):
                if not char == '*':
                    return idx + 1
        return -1

    def __str__(self):
        string_list = self.root_node.to_string_list("")
        string_none_formatted = "\n".join(string_list)
        return string_none_formatted.encode('UTF-8')


def create_empty_ir():
    return InternalRepresentation(("", ""))

def create_ir_using(title, wikitext_content):
    return InternalRepresentation((title, wikitext_content))

class InvalidWikitext(Exception):

    def __init__(self, description):
        super(InvalidWikitext, self).__init__(description)
        self.description = description

    def __str__(self):
        return repr(self.description)


def wikitext_from_json(json_string):
    try:
        json_object = json.loads(json_string)
        page = json_elem_at(json_object, "query.pages")
        page_keys = page.keys()
        page_id = page_keys[0]
        page_internal = page[page_id]
        page_content = page_internal['revisions']
        page_title = page_internal['title']
        page_element = page_content[0]
        return page_title, page_element['*']
    except:
        raise InvalidWikitext("Not a valid JSON string")

def ir_from_json(json_content):
    return InternalRepresentation(wikitext_from_json(json_content))

if __name__ == "__main__":
    pass
