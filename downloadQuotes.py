# coding=UTF-8
import sys
import argparse

from WikiquotesRetriever import *
from IRBuilder import *
from CleanIR import *
from IRToJson import *

def main():
    parser = argparse.ArgumentParser(description="Download all quotes from a certain philosopher")
    parser.add_argument('author', action="store", metavar='author', type=str, help='Name of the author you wish download quotes from')
    parser.add_argument('--raw', action="store_true", dest="raw", help='Show internal representation obtained from wikiquotes with no parsing', default=False)
    args = parser.parse_args()
    philosophers_name = args.author
    wiki_retriever = WikiquotesRetriever()
    wiki_retriever.setup_networking()
    json_content = wiki_retriever.download_quote(philosophers_name)
    wiki_retriever.close_networking()
    wikitext = Wikitext(json_content)
    irinstance = WikitextIR(wikitext)
    if args.raw:
        print irinstance.to_string()
    else:
        remove_noise(irinstance)
        remove_translations(irinstance)
        clean_ir(irinstance)
        json_string = create_json_from_ir(irinstance)
        print json_string.encode('UTF-8')

if __name__ == '__main__':
    main()