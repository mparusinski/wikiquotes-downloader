# coding=UTF-8
import re

COMMON_WORDS_IN_ENGLISH = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have' \
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

COMMON_WORDS_IN_GERMAN = ['das', 'du', 'die', 'ich', 'nicht', 'die', 'es', 'und', 'Sie' \
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

def words_in_text(text):
    return len(text.split(" "))

class LanguageDetector(object):

    def __init__(self):
        self.dictionaries = dict()
        self.__load_dictionaries()
        self._language_regexes = dict()
        self.__compile_regexes()

    def __load_dictionaries(self):
        self.dictionaries['English'] = COMMON_WORDS_IN_ENGLISH
        self.dictionaries['German'] = COMMON_WORDS_IN_GERMAN

    def __compile_regexes(self):
        for key in self.dictionaries.keys():
            current_dictionary = self.dictionaries[key]
            regexes_collection = []
            for word in current_dictionary:
                associated_regex = self.__build_regex_from_word(word)
                regexes_collection.append(associated_regex)
            self._language_regexes[key] = regexes_collection

    def __build_regex_from_word(self, word):
        regex_string = r"(^" + word + ")|(\s" + word + "\s)|(" + word + "$)"
        return re.compile(regex_string)

    def detect_language(self, string):
        language_score_array = dict()
        for key in self.dictionaries.keys():
            language_score = self.score_language(key, string)
            language_score_array[key] = language_score
        return max(language_score_array, key=language_score_array.get)

    def score_language(self, language, string):
        language_regexes = self._language_regexes[language]
        count_total = 0
        for regex in language_regexes:
            matches = len(regex.findall(string))
            count_total = count_total + matches
        return (count_total + 0.0) / words_in_text(string)


def main():
    pass

if __name__ == '__main__':
    main()
