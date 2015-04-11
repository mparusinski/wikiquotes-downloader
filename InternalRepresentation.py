# coding=UTF-8
import json
import re

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

class InvalidIRNodeOperation(Exception):

    def __init__(self, description):
        super(InvalidIRNodeOperation, self).__init__(description)
        self.description = description

    def __str__(self):
        return repr(self.description)


class IRNode(object):
    """Defines a node in the internal representation of a wikitext page"""
    def __init__(self, value, parent_node=None):
        self.value = value
        self.children = []
        self.parent_node = parent_node

    def __eq__(self, other):
        if other == None:
            return False
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
        if ir_node == None:
            msg = "Attempting to add \"None\" to node childrens"
            raise InvalidIRNodeOperation(msg)
        if not (ir_node.parent_node == None or ir_node.parent_node == self):
            msg = "Node (\"ir_node.value\") which already has a parent"
            raise InvalidIRNodeOperation(msg)
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

    def do_for_all_in_tree(self, function):
        for child in self.children:
            child.do_for_all_in_tree(function)
        function(self)

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
        for child in self.children:
            child.parent_node = None
        self.children = []

    def remove_children_using_regex(self, regex):
        children_list_copy = list(self.children) # copy, but not deepcopy
        for child in children_list_copy:
            if regex.match(child.value):
                child.parent_node = None
                self.children.remove(child)

    def remove_child(self, child):
        if child in self.children:
            child.parent_node = None
            self.children.remove(child)

    def remove_nodes_using_regex(self, regex):
        children_list_copy = list(self.children)
        children_stack = list(children_list_copy)
        final_children_list = []
        for child in children_list_copy:
            to_remove = 1
            childrens_to_add = [child]
            if regex.match(child.value):
                to_remove = len(child.children)
                new_children = self.__remove_node_helper(child, children_stack)
                childrens_to_add = new_children[0:to_remove]
            children_stack = children_stack[to_remove:]
            final_children_list = final_children_list + childrens_to_add
        self.children = final_children_list
        self.__repoint_children_to_parent()

    def remove_node(self, node):
        # surgically remove node but not its children
        self.children = self.__remove_node_helper(node, self.children)
        self.__repoint_children_to_parent()

    def __remove_node_helper(self, node, children_state):
        new_children = []
        for child in self.children:
            if child == node:
                child.parent_node = None
                grandchildren = child.children
                new_children = new_children + grandchildren
                child.children = []
            else:
                new_children.append(child)
        return new_children

    def __repoint_children_to_parent(self):
        for child in self.children:
            child.parent_node = self


class InternalRepresentation(object):
    """Defines an internal representation of a wikitext page"""
    def __init__(self, wikitext):
        title, wikitext_content = wikitext
        self.root_node = IRNode(title)
        self.__parse_text(wikitext_content)

    def __eq__(self, other):
        return self.root_node == other.root_node

    def __parse_text(self, text_to_parse):
        valid_line_regex = re.compile(r'^((==)|([*]+))([\s\w])')
        current_node = self.root_node
        current_depth = 0
        for line in text_to_parse.splitlines():
            if valid_line_regex.match(line):
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
        if line.startswith("=="):
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
