import pickle
import os

VERSION_NUMBER = "3.1"
WORD_LIST = "words.txt"
DICT_FILE_NAME = "worddict-" + VERSION_NUMBER + ".p"

def create_dict():
    if not os.path.exists(DICT_FILE_NAME):
        with open(WORD_LIST, 'r') as f:
            words = f.read().lower().split("\n")

        d = {}
        for word in words:
            sorted_word = "".join(sorted(word))
            if sorted_word not in d:
                d[sorted_word] = [word]
            else:
                d[sorted_word].append(word)

        with open(DICT_FILE_NAME, 'w') as outfile:
            pickle.dump(d, outfile)

if __name__ == "__main__":
    create_dict()
    with open(DICT_FILE_NAME, 'r') as dict_file:
        d = pickle.load(dict_file)
    import sys
    if "".join(sorted(sys.argv[1])) in d:
        print d["".join(sorted(sys.argv[1]))]
    else:
        print "Not in dict"