from model import TrigramModel
from parser import parse_data
from anneal import AnagramSolver
from random import sample
import sys

STARTING_TEMPERATURE = 50
STEPS = 1000000
UPDATES = 10


if __name__ == "__main__":
    data = parse_data("data/")
    model = TrigramModel(data)

    found_words = set()
    to_find = sys.argv[1]
    scrambled_word = sample(list(to_find), len(to_find))
    solver = AnagramSolver(model, scrambled_word, found_words)
    solver.Tmax = STARTING_TEMPERATURE
    solver.steps = STEPS
    solver.updates = UPDATES

    word, cost = solver.anneal()
    print ""
    print "\n".join(" ".join(x) for x in sorted(found_words, key=len))
