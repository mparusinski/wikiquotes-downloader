# coding=UTF-8
import sys

from WikiquotesRetriever import *
from IRBuilder import *
from CleanIR import *
from IRToJson import *

if len(sys.argv) > 1:
	try:
		philosophersName = sys.argv[1]
		wikiRetriever = WikiquotesRetriever()
		wikiRetriever.setupNetworking()
		jsonContent = wikiRetriever.downloadQuote(philosophersName)
		wikiRetriever.closeNetworking()
		wikitext = Wikitext(jsonContent)
		irinstance = WikitextIR(wikitext)
		removeNoiseQuotes(irinstance)
		removeTranslations(irinstance)
		cleanIR(irinstance)
		jsonString = createJSONFromIR(irinstance)
		print jsonString
	except:
		print "Exception occurred"
else:
	# TODO Complain about syntax (something better than what is written below)
	print "Syntax is incorrect"