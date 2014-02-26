# import sys
# import getopt
# import os
# import math
import re

def create_dictionary():
  file = open("dictionary.txt")

  line_pattern = '([\w\_\']+)\s([\w\_\']+)'
  dictionary = {}

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
  corpus = []

  while 1:
    line = file.readline()
    if not line:
      break
    line = line.lower()
    line_matches = re.findall(line_pattern, line)
    for match in line_matches:
      corpus.append(match)

  return corpus
    
def main():
  dictionary = create_dictionary()
  corpus = create_corpus()


if __name__ == "__main__":
    main()