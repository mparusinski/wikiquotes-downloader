# coding=UTF-8
import sys
import argparse

from WikiquotesRetriever import WikiquotesRetriever, NetworkingException
from InternalRepresentation import ir_from_json
from CleanIR import remove_noise, remove_translations, clean_ir
from IRToJson import create_json_from_ir

DESCRIPTION = "Download all quotes from a certain philosopher"

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('author', action="store", metavar='author', type=str, \
        help='Name of the author you wish download quotes from')
    parser.add_argument('--raw', action="store_true", dest="raw", \
        help='Show internal representation obtained from wikiquotes with no parsing', \
        default=False)
    parser.add_argument('--from-json', action="store", metavar='json_file', type=str, \
        help='Use JSON file instead of wikiquote API')
    args = parser.parse_args()
    philosophers_name = args.author
    wiki_retriever = WikiquotesRetriever()
    wiki_retriever.setup_networking()
    json_content = ""
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
            json_content = wiki_retriever.download_quote(philosophers_name)
            wiki_retriever.close_networking()
        except NetworkingException as e:
            print e
            return
    irinstance = ir_from_json(json_content)
    if args.raw:
        print irinstance
    else:
        remove_noise(irinstance)
        remove_translations(irinstance)
        clean_ir(irinstance)
        json_string = create_json_from_ir(irinstance)
        print json_string.encode('UTF-8')


if __name__ == '__main__':
    main()
