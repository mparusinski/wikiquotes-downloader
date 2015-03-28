# coding=UTF-8
import sys
import argparse

from WikiquotesRetriever import *
from IRBuilder import *
from CleanIR import *
from IRToJson import *

parser = argparse.ArgumentParser(description="Download all quotes from a certain philosopher")
parser.add_argument('author', action="store", metavar='author', type=str, help='Name of the author you wish download quotes from')
parser.add_argument('--raw', action="store_true", dest="raw", help='Show internal representation obtained from wikiquotes with no parsing', default=False)
args = parser.parse_args()

philosophersName = args.author
wikiRetriever = WikiquotesRetriever()
wikiRetriever.setupNetworking()
jsonContent = wikiRetriever.downloadQuote(philosophersName)
wikiRetriever.closeNetworking()
wikitext = Wikitext(jsonContent)
irinstance = WikitextIR(wikitext)
if args.raw:
    print irinstance.toString()
else:
    removeNoise(irinstance)
    removeTranslations(irinstance)
    cleanIR(irinstance)
    jsonString = createJSONFromIR(irinstance)
    print jsonString.encode('UTF-8')
