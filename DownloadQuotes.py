#!/usr/local/bin/python
# coding=UTF-8
import sys
import argparse

from WikiquotesRetriever import WikiquotesRetriever, NetworkingException
from InternalRepresentation import ir_from_json
from CleanIR import remove_noise, remove_translations, clean_ir
from IRToJson import json_from_ir, combine_json_objects, pretty_format_json

VERSION = 0.8
DESCRIPTION = "wikiquotes-downloader visits wikiquote pages and converts them into a json file\n"
PROGRAMNAME = "wikiquotes-downloader"

class NoAuthorSpecified(Exception):

    def __init__(self, description):
        super(NoAuthorSpecified, self).__init__(description)
        self.description = description

    def __str__(self):
        return repr(self.description)

def main():
    parser = argparse.ArgumentParser(prog=PROGRAMNAME, description=DESCRIPTION)
    parser.add_argument('-a', '--author', action="store", metavar='author', type=str, \
        help='Name of the author you wish download quotes from')
    parser.add_argument('--raw', action="store_true", dest="raw", \
        help='Show internal representation obtained from wikiquotes with no parsing', \
        default=False)
    parser.add_argument('--from-json', action="store", metavar='json_file', type=str, \
        help='Use JSON file instead of wikiquote API')
    parser.add_argument('-o', '--output', action="store", metavar='output_file', type=str, \
        help='Write the quotes to specified file (overwrites)')
    parser.add_argument('-i', '--input', action="store", metavar='input_file', type=str, \
        help='Read author names from input file')
    parser.add_argument('-v', '--version', action="store_true", dest="version", \
        help='Show version number', default=False)
    args = parser.parse_args()
    philosophers_names = []
    if args.version:
        print str(VERSION)
        return
    if args.author:
        print args.author
        philosophers_names.append(args.author)
    elif args.input:
        with open(args.input, "r") as fhandle:
            for line in fhandle:
                author = line.rstrip(" \n")
                philosophers_names.append(author)
    else:
        raise NoAuthorSpecified("You must specified an author using either the --author option or the --input option")
        print parser.print_help()
    wiki_retriever = WikiquotesRetriever()
    wiki_retriever.setup_networking()
    json_contents = []
    if args.from_json:
        try:
            json_file_path = args.from_json
            fhandle = open(json_file_path, "r")
            json_content = fhandle.read()
        except Exception as e:
            print e
            return
    else:
        try:
            for a_philosophers_name in philosophers_names:
                json_contents.append(wiki_retriever.download_quote(a_philosophers_name))
            wiki_retriever.close_networking()
        except NetworkingException as e:
            print e
            return
    irinstances = map(ir_from_json, json_contents)
    final_output = ""
    if args.raw:
        final_output = "\n".join(map(str, irinstances))
    else:
        map(remove_noise, irinstances)
        map(remove_translations, irinstances)
        map(clean_ir, irinstances)
        json_objects = map(json_from_ir, irinstances)
        json_single_object = combine_json_objects(json_objects)
        final_output = pretty_format_json(json_single_object)
    if args.output:
        with open(args.output, "w") as fhandle:
            fhandle.write(final_output)
    else:
        print final_output


if __name__ == '__main__':
    main()
