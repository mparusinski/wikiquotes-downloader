# coding=UTF-8
from InternalRepresentation import InternalRepresentation
from CleanIR import *

class IRNotReady(Exception):

    def __init__(self, detected_issue):
        self.detected_issue = detected_issue

    def __str__(self):
        return repr(self.detected_issue)


def create_json_from_ir(wikitext_ir):
    tab = "  "
    json_string = "{\n" + tab + "\"quotes\": ["
    root_node = wikitext_ir.root_node
    if root_node == None:
        raise IRNotReady("No root node in IR")
    author = root_node.get_string()
    children = root_node.children
    string_list = []
    for child in children:
        quote_text = child.get_string()
        quote_string = tab + tab + "{\n" + tab + tab + tab + "\"quoteText\": \"" + quote_text + "\","
        quote_string = quote_string + "\n" + tab + tab + tab + "\"philosopher\": \"" + author + "\"\n" + tab + tab + "}"
        string_list.append(quote_string)
    internal_string = ",\n".join(string_list)
    json_string = json_string + internal_string + "\n" + tab + "]\n}\n"
    return json_string


if __name__ == '__main__':
    pass
