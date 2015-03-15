#!/bin/sh
QUOTEURL="http://en.wikiquote.org/w/api.php?format=json&action=query&titles=Friedrich%20Nietzsche&prop=revisions&rvprop=content"
curl $QUOTEURL > Friedrich_Nietzsche.json