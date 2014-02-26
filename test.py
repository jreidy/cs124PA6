# import sys
# import getopt
# import os
# import math
import re
    
def main():
  file = open("dictionary.txt")

  line_pattern = '([\w\_\']+)\s([\w\_\']+)'
  words = {}

  repeats = 0
  while 1:
      line = file.readline()
      if not line:
        break
      line = line.lower()
      line_matches = re.findall(line_pattern, line)
      for match in line_matches:
        check_exist = words.get(match[0], " ")
        if check_exist != " ":
          repeats = repeats + 1
        words[match[0]] = match[1]

  print len(words)
  print repeats


if __name__ == "__main__":
    main()