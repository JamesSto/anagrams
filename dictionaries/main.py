from create_dict import create_dict, DICT_FILE_NAME
import pickle
import json
from string import ascii_lowercase
from sys import stdin
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

def get_anagrams(target_list):
    solutions = set()
    for x in get_combinations(target_list):
        s = "".join(sorted(x))
        if s in d:
            for word in d[s]:
                solutions.add(word)
    return solutions

def get_anagrams_with_spaces(target_list):
    if len(target_list) == 1:
        return set()
    solutions = set()
    # After going halfway through, we're just generating the same combinations but reversed
    # We can rely on the user to distinguish them at the point
    for n in xrange(1, (len(target_list)+1)/2+1):
        # We want to put the space everywhere it can go, so we split up the list in every single possible way it can
        # be split into two groups (between this loop and the above)
        for sub in itertools.combinations(target_list, n):
            sub = list(sub)
            # Create "the other half" of the targets
            remainder = list(target_list)
            for item in sub:
                remainder.remove(item)
            sub_anagrams = get_anagrams_with_spaces(sub) | get_anagrams(sub)
            remainder_anagrams = get_anagrams_with_spaces(remainder) | get_anagrams(remainder)
            for w1 in sub_anagrams:
                for w2 in remainder_anagrams:
                    solutions.add(w1 + " " + w2)
    return solutions

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
    parser.add_argument("--spaces", 
                        default=False,
                        action="store_const",
                        const=True,
                        help="Include anagrams that have spaces in them")
    args = parser.parse_args()

    target_json = json.loads(args.target_json.read())
    target_list = target_json["found_targets"]
    max_unknowns = target_json["max_unknowns"]
    
    for _ in xrange(max_unknowns+1):
        if not args.spaces:
            anagrams = get_anagrams(target_list)
        else:
            anagrams = get_anagrams_with_spaces(target_list) | get_anagrams(target_list)

        for ana in anagrams:
            print ana
        target_list.append(ascii_lowercase)
    
