# coding=UTF-8
import json
from InternalRepresentation import InternalRepresentation
from CleanIR import *

class IRNotReady(Exception):

    def __init__(self, detected_issue):
        self.detected_issue = detected_issue

    def __str__(self):
        return repr(self.detected_issue)

def json_from_ir(wikitext_ir):
    json_obj = dict()
    root_node = wikitext_ir.root_node
    if root_node == None:
        raise IRNotReady("No root node in IR")
    author = root_node.value
    children = root_node.children
    subobjects = []
    for child in children:
        quote_text = child.value
        subobjects.append({"quoteText": quote_text, "philosopher": author})
    json_obj["quotes"] = subobjects
    return json_obj

def combine_json_objects(json_objects):
    total_quotes_list = []
    for json_obj in json_objects:
        quotes = json_obj["quotes"]
        total_quotes_list = total_quotes_list + quotes
    return {"quotes": total_quotes_list}

def pretty_format_json(json_obj):
    return json.dumps(json_obj, indent=4, sort_keys=True).decode('UTF-8')

if __name__ == '__main__':
    pass
