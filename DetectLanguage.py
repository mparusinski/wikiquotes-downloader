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

def matchLanguage(text, languageCommonWords):
	countTotal = 0
	for word in languageCommonWords:
		wordRegex = r"(^" + word + ")|(\s" + word + "\s)|(" + word + "$)"
		matches = len(re.findall(wordRegex, text))
		countTotal = countTotal + len(re.findall(wordRegex, text))
	return (countTotal + 0.0) / wordsInText(text)

def detectLanguage(text):
	englishScore = matchLanguage(text, commonWordsEnglish)
	germanScore = matchLanguage(text, commonWordsGerman)
	if englishScore > germanScore:
		return "English"
	else:
		return "German"

def main():
	print matchLanguage("Once upon a time there was a sausage called Baldrick", commonWordsGerman)
	print matchLanguage("Il etait une fois une saucisse nomme Baldrick", commonWordsGerman)

if __name__ == '__main__':
	main()
