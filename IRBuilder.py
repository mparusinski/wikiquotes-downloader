# coding=UTF-8
import json
import re
from StringIO import StringIO

def inspectJSONObject(json):
    for key in json.iterkeys():
        stringObjectValue = unicode(json[key])
        print key + ": " + stringObjectValue[0:100]

def inspectJSONList(json):
    for elem in json:
        stringElem = unicode(elem)
        print stringElem[0:100]


class WikitextIRNode(object):
    """Defines a node in the internal representation of a wikitext page"""
    def __init__(self, currentString, parentNode = None):
        self.currentString = currentString
        self.children = []
        self.parentNode = parentNode

    def addChild(self, wikitextIRNode):
        self.children.append(wikitextIRNode)

    def setString(self, newString):
        self.currentString = newString

    def getParent(self):
        return self.parentNode

    def getChildren(self):
        return self.children

    def getString(self):
        return self.currentString

    def toStringList(self, tabulation):
        """Build a list of strings"""
        firstItem = tabulation + self.currentString
        accum = [firstItem]
        for child in self.children:
            childStringList = child.toStringList(tabulation + "  ")
            accum = accum + childStringList
        return accum

    def toString(self):
        stringList = self.toStringList("")
        return "\n".join(stringList)

    def doForAllAncestry(self, function):
        for child in self.children:
            function(child)
            child.doForAllAncestry(function)

    def findChildrenUsingRegex(self, regex):
        # assuming regex is precompiled
        foundList = []
        for child in self.children:
            if regex.match(child.getString()):
                foundList.append(child)
        return foundList

    def findChildrenUsingFunction(self, function):
        foundList = []
        for child in self.children:
            if function(child):
                foundList.append(child)
        return foundList

    def removeChildren(self):
        self.children = []

    def removeChildrenUsingRegex(self, regex):
        childrenListCopy = list(self.children) # copy, but not deepcopy
        for child in childrenListCopy:
            if regex.match(child.getString()):
                self.children.remove(child)

    def removeChild(self, child):
        self.children.remove(child)

    def removeNodesUsingRegex(self, regex):
        childrenListCopy = list(self.children)
        for child in childrenListCopy:
            if regex.match(child.getString()):
                self.removeChildNode(child)

    def removeChildNode(self, node):
        # surgically remove node but not its children
        nodesChildren = node.getChildren()
        for nodesChild in nodesChildren:
            nodesChild.parentNode = self
        nodesIndex = self.children.index(node)
        newChildren = []
        for child in self.children:
            if child == node:
                newChildren = newChildren + nodesChildren
            else:
                newChildren.append(child)
        self.children = newChildren


class WikitextIR:
    """Defines an internal representation of a wikitext page"""
    def __init__(self, wikitext):
        self.rootNode = WikitextIRNode(wikitext.getWikitextTitle())
        self.__parseText(wikitext.getWikitextString())

    def __parseText(self, textToParse):
        currentNode = self.rootNode
        currentDepth = 0
        for line in textToParse.splitlines():
            if self.__validLine(line):
                depth = self.__findDepth(line)
                if depth > currentDepth: # Going deeper
                    if not (depth - currentDepth == 1):
                        # TODO Raise appropriate error
                        print "Parse error! Line " + line + " is not invalid"
                    else:
                        newNode = WikitextIRNode(line, parentNode=currentNode)
                        currentNode.addChild(newNode)
                        currentNode = newNode
                        currentDepth = depth
                else:
                    dropAmount = currentDepth - depth
                    for i in xrange(dropAmount):
                        currentNode = currentNode.getParent()
                    parentNode = currentNode.getParent()
                    newNode = WikitextIRNode(line, parentNode=parentNode)
                    parentNode.addChild(newNode)
                    currentNode = newNode
                    currentDepth = depth

    def __validLine(self, line):
        return line.startswith("== ") or (len(line) > 0 and line[0] == '*')

    def __findDepth(self, line):
        if line.startswith("== "):
            return 1
        else:
            for idx, char in enumerate(line):
                if not char == '*':
                    return idx + 1
        return -1

    def getRoot(self):
        return self.rootNode

    def toString(self):
        stringList = self.rootNode.toStringList("")
        stringNoneFormatted = "\n".join(stringList)
        return stringNoneFormatted.encode('UTF-8')


class InvalidWikitext(Exception):

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return repr(self.description)

class Wikitext(object):
    """Wikitext that is embedded in a jsonString"""
    def __init__(self, jsonString):
        self.nodes = []
        self.keyString = "query.pages"
        self.pageTitle = None
        self.wikitext = None
        self.__extractWikitext(jsonString)

    def __processPage(self, page):
        pageKeys = page.keys()
        pageID = pageKeys[0]
        pageInternal = page[pageID]
        self.pageTitle = pageInternal['title']
        pageContent = pageInternal['revisions']
        pageElement = pageContent[0]
        self.wikitext = pageElement["*"]

    def __extractWikitext(self, jsonString):
        try:
            jsonContent = json.loads(jsonString)
            page = self.__getAddressJSON(jsonContent, self.keyString)
            self.__processPage(page)
        except ValueError:
            raise InvalidWikitext("Not a valid JSON file")

    def __getAddressJSON(self, json, addressString):
        tokens = addressString.split('.')
        jsonContent = json
        for token in tokens:
            jsonContent = jsonContent[token]
        return jsonContent

    def getWikitextString(self):
        return self.wikitext

    def getWikitextTitle(self):
        return self.pageTitle

def main():
    with open('baselines/Friedrich_Nietzsche.json', 'r') as filehandle:
        externalJSONContent = filehandle.read()
        wikitext = Wikitext(externalJSONContent)
        irinstance = WikitextIR(wikitext)
        print irinstance.toString()

if __name__ == "__main__":
    main()
        