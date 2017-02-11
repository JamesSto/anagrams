from create_dict import create_dict, DICT_FILE_NAME
import pickle
import json
from string import ascii_lowercase
from sys import argv, stdin
import itertools
import argparse


def combos(letter, target_list):
    for x in get_combinations(target_list[1:]):
        yield letter + x


def get_combinations(target_list):
    if not target_list:
        return [""]

    combinations = []
    for letter in target_list[0]:
        combinations = itertools.chain(combinations, combos(letter, target_list))

    return combinations

if __name__ == "__main__":
    create_dict()
    with open(DICT_FILE_NAME, 'r') as dict_file:
        d = pickle.load(dict_file)

    parser = argparse.ArgumentParser("Finds possible anagrams given found targets and possible targets still existing")
    parser.add_argument('target_json', 
                        nargs='?', 
                        type=argparse.FileType('r'), 
                        default=stdin, 
                        help="JSON file representing the targets found and expected")
    args = parser.parse_args()

    target_json = json.loads(args.target_json.read())
    target_list = target_json["found_targets"]
    max_unknowns = target_json["max_unknowns"]
    memo = {}
    solutions = set()
    for _ in xrange(max_unknowns):
        for x in get_combinations(target_list):
            s = "".join(sorted(x))
            if s in d:
                for word in d[s]:
                    if word not in solutions:
                        print word
                        solutions.add(word)
        target_list.append(ascii_lowercase)