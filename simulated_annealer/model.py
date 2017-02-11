from __future__ import division
from collections import Counter
from string import ascii_lowercase
from itertools import product

class TrigramModel(object):

    def __init__(self, train_data):
        '''Takes in a list of strings to train on, 
        uses trigram probability with add one smoothing'''
        self.trigram_counts = Counter()

        for s in train_data:
            # We start with a space because each word should start with a space 
            # the anagram will be seeded with a space
            s = " " + s
            self.trigram_counts.update(zip(s, s[1:], s[2:]))

        # Add-one smoothing - could be done more efficiently but with only 27 tokens, this is reasonable
        tokens = ascii_lowercase + " "
        for letters in product(tokens, tokens, tokens):
            self.trigram_counts[tuple(letters)] += 1


        self.bigram_counts = Counter()
        for c1,c2,c3 in self.trigram_counts:
            self.bigram_counts[c1,c2] += self.trigram_counts[c1,c2,c3]

    def get_probability(self, letters):
        letters = tuple(letters)
        return self.trigram_counts[letters]/self.bigram_counts[letters[0],letters[1]]


if __name__ == "__main__":
    from parser import parse_data
    from sys import argv

    data = parse_data("data/")
    model = TrigramModel(data)
    print model.get_probability(argv[1])