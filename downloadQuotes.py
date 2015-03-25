import sys

from WikiquotesRetriever import *
from IRBuilder import *
from IRTransformation import *
from CleanIR import *
from IRToJson import *

if len(sys.argv) > 1:
	philosophersName = sys.argv[1]
	wikiRetriever = WikiquotesRetriever()
	wikiRetriever.setupNetworking()
	jsonContent = wikiRetriever.downloadQuote(philosophersName)
	wikiRetriever.closeNetworking()
	wikitext = Wikitext(jsonContent)
	irinstance = WikitextIR(wikitext)
	# Technically they should work on both on the same instance
	removeNoiseQuotes(irinstance)
	removeTranslations(irinstance)
	cleanIR(irinstance)
	jsonString = createJSONFromIR(irinstance)
	print jsonString
else:
	# TODO Complain about syntax (something better than what is written below)
	print "Syntax is incorrect"