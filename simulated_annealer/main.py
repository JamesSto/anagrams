from model import TrigramModel
from parser import parse_data
from anneal import AnagramSolver
from random import sample

STARTING_TEMPERATURE = 50
STEPS = 10000
UPDATES = 10


if __name__ == "__main__":
    data = parse_data("data/")
    model = TrigramModel(data)

    found_words = set()
    to_find = "cuttlefishes"
    scrambled_word = sample(list(to_find), len(to_find))
    solver = AnagramSolver(model, scrambled_word, found_words)
    solver.Tmax = STARTING_TEMPERATURE
    solver.steps = STEPS
    solver.updates = UPDATES

    word, cost = solver.anneal()
    print scrambled_word
    print word
    print found_words