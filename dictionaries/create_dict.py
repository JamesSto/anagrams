import pickle
import os

VERSION_NUMBER = "1.1"
WORD_LIST = "words.txt"
DICT_FILE_NAME = "worddict-" + VERSION_NUMBER + ".p"

def create_dict():
    if not os.path.exists(DICT_FILE_NAME):
        with open("/usr/share/dict/words", 'r') as f:
            words = f.read().lower().split()

        d = {}
        for word in words:
            if word not in d:
                d["".join(sorted(word))] = [word]
            else:
                d["".join(sorted(word))].append(word)

        with open(DICT_FILE_NAME, 'w') as outfile:
            pickle.dump(d, outfile)
