from create_dict import create_dict, DICT_FILE_NAME
import pickle
import json
from string import ascii_lowercase
from sys import argv
from tqdm import tqdm
import itertools


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

    if len(argv) > 1:
        if argv[1].endswith(".json"):
            with open(argv[1], 'r') as target_json:
                target_json = json.loads(target_json.read())
                target_list = target_json["found_targets"]
                max_unknowns = target_json["max_unknowns"]
                memo = {}
                solutions = []
                for _ in tqdm(xrange(max_unknowns)):
                    for x in get_combinations(target_list):
                        s = "".join(sorted(x))
                        if s in d:
                            solutions += d[s]
                    target_list.append(ascii_lowercase)
                print set(solutions)
        else:
            word = argv[1]