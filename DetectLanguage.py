# coding=UTF-8
import re
import os

def read_dictionary(filepath):
  dictionary = []
  with open(filepath, 'r') as fhandle:
    for line in fhandle:
      word = line.rstrip("\n")
      dictionary.append(word)
  return dictionary

def words_in_text(text):
    return len(text.split(" "))

class LanguageDetector(object):

    def __init__(self):
        self.dictionaries = dict()
        self.__load_dictionaries()
        self._language_regexes = dict()
        self.__compile_regexes()

    def __load_dictionaries(self):
      directory_name = "dictionaries"
      valid_dictionaries_regex = re.compile(r'^[\w]+\.txt$')
      for file_name in os.listdir(directory_name):
        if valid_dictionaries_regex.match(file_name):
          file_path = directory_name + '/' + file_name
          dictionary_name = file_name[:-len(".txt")]
          self.dictionaries[dictionary_name] = read_dictionary(file_path)

    def __compile_regexes(self):
        for key in self.dictionaries.keys():
            current_dictionary = self.dictionaries[key]
            regexes_collection = []
            for word in current_dictionary:
                associated_regex = self.__build_regex_from_word(word)
                regexes_collection.append(associated_regex)
            self._language_regexes[key] = regexes_collection

    def __build_regex_from_word(self, word):
        regex_string = r"(^" + word + ")|(\s" + word + r"\s)|(" + word + "$)"
        return re.compile(regex_string, re.IGNORECASE)

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


if __name__ == '__main__':
    pass
