
import codecs
import re
import nltk

corpus = []
translation = []

tree_dict = {}

dictionary = {}
pos_dictionary={}
test_set = [0,1,2,3,4]

_digits = re.compile('\d')
def contains_digits(d):
  return bool(_digits.search(d))

_punctuation = re.compile('[\.\:\!\,]')
def contains_punctuation(d):
  return bool(_punctuation.search(d))

_underscore = re.compile('_')
def contains_underscore(d):
  return bool(_underscore.search(d))

def translate():

  for sentence in corpus:
    translated_sentence = ""
    list_sentence = sentence.split()

    for word in list_sentence:
      # check for punctuation and add if found at end
      punctuation = ""
      if contains_punctuation(word):
        punctuation = word[-1:]
        word = word[:-1]
      # split on apostrophe
      if "'" in word:
        list_word = word.split("'")
        for cur_word in list_word:
          translated_sentence += " " + dictionary[cur_word]
      # if digits just append
      elif contains_digits(word):
        translated_sentence += " " + word
      # default lookup case
      else:
        english_word = dictionary[word]
        if contains_underscore(english_word):
          english_word = english_word.replace("_", " ")
        translated_sentence += " " + english_word
      # punctuation is usually empty
      translated_sentence += punctuation

    translation.append(translated_sentence)

def create_dictionary():

  file = codecs.open("dictionary.txt", 'r', encoding='utf-8')
  
  while 1:
      line = file.readline()
      if not line:
        break
      line = line.lower()
      list_pair = line.split()
      dictionary[list_pair[0]] = list_pair[1]

  return dictionary

def create_corpus():
  file = codecs.open("corpus.txt", 'r', encoding='utf-8')

  while 1:
    line = file.readline()
    if not line:
      break
    line = line.lower()
    corpus.append(line)
    
def create_tree_dict():
  file = codecs.open("tagfile.txt", 'r', encoding='utf-8')
  print 'function called'
  while 1:
    line = file.readline()
    split_line = line.split()
    if split_line and len(split_line) == 3:
      tree_dict[split_line[0].replace("'","")] = [split_line[1],split_line[2]]

    if not line:
      break
    line = line.lower()
    corpus.append(line)

  print tree_dict

def main():
  create_dictionary()
  create_corpus()
  translate()
  create_tree_dict()

  i = 0

  
  f = open('POS_dict','w')
  #f.write('hi there\n') # python will convert \n to os.linesep
   # you can omit in most cases as the destructor will call if
  

  for sentence in translation:
    # print sentence
    # print ""
    # print corpus[i]
    i += 1
    # print ""
    # print 'nltk'

    #run once
    #nltk.download('maxent_treebank_pos_tagger');
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    for  tag in tagged:
      dict_string = tag[1] + " " +  tag[0] + '\n'
      f.write(dict_string)
      pos_dictionary[tag[0]] = tag[1] 

    print 
    print

  f.close()
  print pos_dictionary

if __name__ == "__main__":
    main()