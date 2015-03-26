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

def wordsInText(text):
	return len(text.split(" "))

def matchLanguage(text, languageCommonWords):
	countTotal = 0
	for word in languageCommonWords:
		wordRegex = r"(^" + word + ")|(\s" + word + "\s)|(" + word + "$)"
		matches = len(re.findall(wordRegex, text))
		countTotal = countTotal + len(re.findall(wordRegex, text))
	return (countTotal + 0.0) / wordsInText(text)

def main():
	print matchLanguage("Once upon a time there was a sausage called Baldrick", commonWordsEnglish)
	print matchLanguage("Il etait une fois une saucisse nomme Baldrick", commonWordsEnglish)

if __name__ == '__main__':
	main()