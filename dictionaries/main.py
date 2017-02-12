from create_dict import create_dict, DICT_FILE_NAME
import pickle
import json
from string import ascii_lowercase
from sys import stdin
from tqdm import tqdm
import itertools
import argparse

MAX_DEPTH = 2

def calc_entropy(target_list):
    return reduce(lambda x,y : x*y, map(len, target_list), 1)

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

def get_anagrams(target_list, d, spaces=False, depth=0):
    solutions = set()
    # Only show the progress bar if we're not in a recursive call and it's going to take long enough that it'll be worth showing
    if depth == 0 and calc_entropy(target_list) > 1000:
        looper = tqdm(get_combinations(target_list), total=calc_entropy(target_list))
    else:
        looper = get_combinations(target_list)
    for x in looper:
        s = "".join(sorted(x))
        if not spaces or len(s) == 1 or depth >= MAX_DEPTH:
            if s in d:
                for word in d[s]:
                    solutions.add(word)
        else:
            for n in xrange(1, (len(target_list)+1)/2+1):
                for sub in itertools.combinations(s, n):
                    sub = list(sub)
                    # Create "the other half" of the targets
                    remainder = list(s)
                    for item in sub:
                        remainder.remove(item)
                    sub_anagrams = get_anagrams(sub, d, spaces=True, depth=depth+1) | get_anagrams(sub, d, depth=1)
                    remainder_anagrams = get_anagrams(remainder, d, spaces=True, depth=depth+1) | get_anagrams(remainder, d, depth=1)
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
        anagrams = get_anagrams(target_list, d)
        if args.spaces:
            anagrams |= get_anagrams(target_list, d, spaces=True) 
        for ana in anagrams:
            print ana
        target_list.append(ascii_lowercase)
    
