
import codecs
import re
import nltk

# list of italian sentences
corpus = []
# list of translations
translation = []
# dictionary of terms mapping italian -> english
dictionary = {}
# english part of speech 
pos_dictionary={}

translation_split = []

test_set_indices = [0,1,2,3,4]

_digits = re.compile('\d')
def contains_digits(d):
  return bool(_digits.search(d))

_punctuation = re.compile('[\.\:\!\,]')
def contains_punctuation(d):
  return bool(_punctuation.search(d))

_underscore = re.compile('_')
def contains_underscore(d):
  return bool(_underscore.search(d))

def apply_adjective_noun_strategy(sentence):
  # list of indexes that need to be flipped after iteration over sentence
  flipping_indexes = []
  # compare word pairs- end w/ penultimate index
  for i in range(0, len(sentence)-2):
    first_word = sentence[i]
    second_word = sentence[i+1]
    if contains_punctuation(first_word) or contains_punctuation(second_word) or contains_digits(first_word) or contains_digits(second_word):
      continue
    if pos_dictionary[first_word] == "NN" and pos_dictionary[second_word] == "JJ":
      flipping_indexes.append(i)
  return_sentence = sentence
  for index in flipping_indexes:
    temp_word = return_sentence[index]
    return_sentence[index] = return_sentence[index+1]
    return_sentence[index+1] = temp_word

  return return_sentence

def apply_processing_strategies():
  index = 1
  processed_sentences = []
  for sentence in translation_split:
    print index
    index += 1
    working_sentence = sentence
    working_sentence = apply_adjective_noun_strategy(working_sentence)
    processed_sentences.append(working_sentence)

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
      dict_string = tag[1] + " " +  tag[0] + '\n'
      f.write(dict_string)
      pos_dictionary[tag[0]] = tag[1]

  f.close()

def translate():

  for sentence in corpus:
    translated_sentence = ""
    list_sentence = sentence.split()

    translated_sentence_list = []
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
          translated_sentence += " " + dictionary[cur_word]
          translated_sentence_list.append(dictionary[cur_word])
      # if digits just append
      elif contains_digits(word):
        translated_sentence += " " + word
        translated_sentence_list.append(word)
      # default lookup case
      else:
        english_word = dictionary[word]
        if contains_underscore(english_word):
          english_word = english_word.replace("_", " ")
        translated_sentence += " " + english_word
        split_english_word = english_word.split()
        for split_word in split_english_word:
          translated_sentence_list.append(split_word)
      # punctuation is usually empty
      translated_sentence += punctuation
      if has_punctuation:
        translated_sentence_list.append(punctuation)

    translation.append(translated_sentence)
    translation_split.append(translated_sentence_list)

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
    
def main():
  create_dictionary()
  create_corpus()
  translate()
  create_english_pos()
  apply_processing_strategies()

if __name__ == "__main__":
    main()