# coding=UTF-8
import re

commonWordsEnglish = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have' \
					 , 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you' \
					 , 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they' \
					 , 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one' \
					 , 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out' \
					 , 'if', 'about', 'who', 'get', 'which', 'go', 'make', 'can' \
					 , 'like', 'time', 'know', 'just', 'him', 'take', 'people', 'into' \
					 , 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other' \
					 , 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over' \
					 , 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our' \
					 , 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because' \
					 , 'any', 'these', 'give', 'day', 'most']

commonWordsGerman = ['das', 'du', 'die', 'ich', 'nicht', 'die', 'es', 'und', 'Sie' \
					, 'der', 'was', 'wir', 'zu', 'ein', 'er', 'in', 'sie', 'mir', 'mit' \
					, 'ja', 'wie', 'den', 'auf', 'mich', 'dass', 'so', 'hier', 'ein' \
					, 'wenn', 'hat', 'all', 'sind', 'von', 'dich', 'war', 'haben', 'für' \
					, 'an', 'habe', 'da', 'nein', 'bin', 'noch', 'dir', 'uns', 'sich' \
					, 'nur', 'einen', 'kann', 'dem', 'auch', 'schon', 'als', 'dann', 'ihn' \
					, 'mal', 'hast', 'sein', 'ihr', 'aus', 'um', 'aber', 'meine', 'Aber' \
					, 'wir', 'doch', 'mein', 'bist', 'im', 'keine', 'gut', 'oder', 'weiß' \
					, 'jetzt', 'man', 'nach', 'werden', 'wo', 'Oh', 'will', 'also', 'mehr' \
					, 'immer', 'muss', 'warum', 'bei', 'etwas', 'nichts', 'bitte', 'wieder' \
					, 'machen', 'diese', 'vor', 'können', 'hab', 'zum', 'gehen', 'sehr' \
					, 'geht', 'sehen']

def wordsInText(text):
	return len(text.split(" "))

class LanguageDetector:

	def __init__(self):
		self.dictionaries = dict()
		self.__loadDictionaries__()
		self.__languageRegexes__ = dict()
		self.__compileRegexes__()

	def __loadDictionaries__(self):
		self.dictionaries['English'] = commonWordsEnglish
		self.dictionaries['German'] = commonWordsGerman

	def __compileRegexes__(self):
		for key in self.dictionaries.keys():
			currentDictionary = self.dictionaries[key]
			regexesCollection = []
			for word in currentDictionary:
				associatedRegex = self.__buildRegexFromWord__(word)
				regexesCollection.append(associatedRegex)
			self.__languageRegexes__[key] = regexesCollection

	def __buildRegexFromWord__(self, word):
		regexString = r"(^" + word + ")|(\s" + word + "\s)|(" + word + "$)"
		return re.compile(regexString)

	def detectLanguage(self, string):
		languageScoreArray = dict()
		for key in self.dictionaries.keys():
			languageScore = self.scoreLanguage(key, string)
			languageScoreArray[key] = languageScore
		return max(languageScoreArray, key=languageScoreArray.get)

	def scoreLanguage(self, language, string):
		languageRegexes = self.__languageRegexes__[language]
		countTotal = 0
		for regex in languageRegexes:
			matches = len(regex.findall(string))
			countTotal = countTotal + matches
		return (countTotal + 0.0) / wordsInText(string)


def main():
	pass

if __name__ == '__main__':
	main()
