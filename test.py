import codecs
import re
import nltk
import copy

# list of italian sentences
corpus = []
# list of translations
translation = []
# dictionary of terms mapping italian -> english
tree_dict = {}

dictionary = {}
# english part of speech 
pos_dictionary={}

# italian split
sentence_split = []

translation_split = []

_digits = re.compile('\d')
def contains_digits(d):
  return bool(_digits.search(d))

_punctuation = re.compile('[\.\:\!\,]')
def contains_punctuation(d):
  return bool(_punctuation.search(d))

_underscore = re.compile('_')
def contains_underscore(d):
  return bool(_underscore.search(d))

def apply_not_strategy(sentence):
  flipping_indexes = []
  for i in range(0, len(sentence)-1):
    if sentence[i] == 'not':
      flipping_indexes.append(i)
  for index in flipping_indexes:
    new_word = ""
    next_word = pos_dictionary[sentence[index+1]]
    if next_word == "VB":
      new_word = "do_"
    elif next_word == "VBD":
      new_word = "do_"
    elif next_word == "VBZ":
      new_word = "does_"
    elif next_word == "VBG":
      # gerund should not change
      new_word = ""
    elif next_word == "VBN":
      new_word = ""
    elif next_word == "VBP":
      new_word = "does_"
    else:
      new_word = ""

    sentence[index] = new_word + 'not'

def apply_adjective_noun_strategy(sentence):
  # list of indexes that need to be flipped after iteration over sentence
  flipping_indexes = []
  # compare word pairs- end w/ penultimate index
  for i in range(0, len(sentence)-2):
    first_word = sentence[i]
    second_word = sentence[i+1]
    if contains_punctuation(first_word) or contains_punctuation(second_word) or contains_digits(first_word) or contains_digits(second_word):
      continue
    if (pos_dictionary[first_word] == "NN" or pos_dictionary[first_word] == "NNS" ) and pos_dictionary[second_word] == "JJ":
      flipping_indexes.append(i)
  # manipulate sentence accordingly
  for index in flipping_indexes:
    temp_word = sentence[index]
    sentence[index] = sentence[index+1]
    sentence[index+1] = temp_word

def apply_post_processing_strategies():
  index = 1
  processed_english_sentences = []
  for sentence in translation_split:
    print index
    index += 1
    # we must copy the list and it's objects (deep)
    working_sentence = copy.deepcopy(sentence)

    apply_adjective_noun_strategy(working_sentence)
    apply_not_strategy(working_sentence)
    print working_sentence
    processed_english_sentences.append(working_sentence)

def apply_adverb_verb_strategy(sentence):
    # list of indexes that need to be flipped after iteration over sentence
  flipping_indexes = []
  # compare word pairs- end w/ penultimate index
  for i in range(0, len(sentence)-2):
    first_word = sentence[i]
    second_word = sentence[i+1]
    if contains_punctuation(first_word) or contains_punctuation(second_word) or contains_digits(first_word) or contains_digits(second_word):
      continue
    pos_1 = tree_dict.get(first_word, "")
    pos_2 = tree_dict.get(second_word, "")
    if pos_1 != "" and pos_2 != "":
      if "ver" in pos_1[0] and pos_2[0] == "adv":
        flipping_indexes.append(i)
        print first_word
  # manipulate sentence accordingly
  for index in flipping_indexes:
    temp_word = sentence[index]
    sentence[index] = sentence[index+1]
    sentence[index+1] = temp_word

def apply_pre_processing_strategies():
  index = 1
  processed_sentence_split = []
  for sentence in sentence_split:
    print index
    index += 1

    working_sentence = copy.deepcopy(sentence)
    apply_adverb_verb_strategy(working_sentence)
    processed_sentence_split.append(working_sentence)

  for i in range(0, len(processed_sentence_split)):
    sentence_split[i] = processed_sentence_split[i]

def split_italian():
  for sentence in corpus:
    list_sentence = sentence.split()

    italian_sentence_list = []
    for word in list_sentence:
      # check for punctuation and add if found at end
      has_punctuation = False
      punctuation = ""
      if contains_punctuation(word):
        punctuation = word[-1:]
        word = word[:-1]
        has_punctuation = True
      # split on apostrophe
      if "'" in word:
        list_word = word.split("'")
        for cur_word in list_word:
          italian_sentence_list.append(cur_word)
      # if digits just append
      elif contains_digits(word):
        italian_sentence_list.append(word)
      # default lookup case
      else:
        italian_sentence_list.append(word)
      # punctuation is usually empty
      if has_punctuation:
        italian_sentence_list.append(punctuation)

    sentence_split.append(italian_sentence_list)

def translate_from_split():
  for sentence in sentence_split:
    translated_sentence_list = []
    translated_sentence = ""
    for word in sentence:
      if contains_digits(word):
        translated_sentence_list.append(word)
        translated_sentence += " " + word
      elif contains_punctuation(word):
        translated_sentence_list.append(word)
        translated_sentence += word
      else:
        english_word = dictionary[word][0]
        print english_word
        if contains_underscore(english_word):
          english_word = english_word.replace("_", " ")
        translated_sentence += " " + english_word
        split_english_word = english_word.split()
        for split_word in split_english_word:
          translated_sentence_list.append(split_word)
    translation_split.append(translated_sentence_list)
    translation.append(translated_sentence)

def create_dictionary():

  file = codecs.open("dictionary_multiple_def.txt", 'r', encoding='utf-8')
  
  while 1:
      line = file.readline()
      if not line:
        break
      line = line.lower()
      list_pair = line.split()
      new_word_list = []
      translated_words = list_pair[1].split(",")
      for word in translated_words:
        new_word_list.append(word)
      dictionary[list_pair[0]] = new_word_list

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
  while 1:
    line = file.readline()
    if not line:
      break
    line = line.lower()
    split_line = line.split()
    if split_line and len(split_line) == 3:
      tree_dict[split_line[0].replace("'","")] = [split_line[1],split_line[2]]


def create_english_pos():
  
  f = open('POS_dict','w')
  #f.write('hi there\n') # python will convert \n to os.linesep
  # you can omit in most cases as the destructor will call if

  for sentence in translation:
    #run once
    #nltk.download('maxent_treebank_pos_tagger');
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    for  tag in tagged:
      dict_string =  tag[0] + '[ ' + tag[1] + ' ]' + ' '
      f.write(dict_string)
      pos_dictionary[tag[0]] = tag[1]

    f.write('\n')

  f.close()

def main():
  create_dictionary()
  create_corpus()
  split_italian()
  create_tree_dict()
  apply_pre_processing_strategies()
  translate_from_split()
  create_english_pos()
  apply_post_processing_strategies()

if __name__ == "__main__":
    main()