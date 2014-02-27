# import sys
# import getopt
# import os
# import math
import re

corpus = []
translation = []
dictionary = {}
test_set = [0,1,2,3,4]

# guardando looking
# vuoto empty

def translate():

  line_pattern = "([\w']+)"

  for sentence in corpus:
    translated_sentence = ""
    split_sentence = re.findall(line_pattern, sentence)
    print split_sentence
    for word in split_sentence:
      translated_sentence = translated_sentence + dictionary[word]
    translation.append(translated_sentence)

def create_dictionary():
  file = open("dictionary.txt")

  line_pattern = '([\w\_\']+)\s([\w\_\']+)'
  
  repeats = 0
  while 1:
      line = file.readline()
      if not line:
        break
      line = line.lower()
      line_matches = re.findall(line_pattern, line)
      for match in line_matches:
        check_exist = dictionary.get(match[0], " ")
        if check_exist != " ":
          repeats = repeats + 1
        dictionary[match[0]] = match[1]

  # print len(dictionary)
  # print repeats
  return dictionary

def create_corpus():
  file = open("corpus.txt")

  line_pattern = '(.+)'

  while 1:
    line = file.readline()
    if not line:
      break
    line = line.lower()
    line_matches = re.findall(line_pattern, line)
    for match in line_matches:
      corpus.append(match)
    
def main():
  create_dictionary()
  create_corpus()
  translate()
  print translation

if __name__ == "__main__":
    main()