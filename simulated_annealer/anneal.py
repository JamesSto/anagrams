from __future__ import division
from simanneal import Annealer
from random import shuffle, randrange, random
from math import log

class AnagramSolver(Annealer):

    SPACE_FREQUENCY = .0001

    def __init__(self, model, letters, found_words):
        # This way we can take in basically any iterable
        self.state = list(letters)
        self.num_letters = len(self.state)
        self.model = model
        self.found_words = found_words
        # Start from a random position to remove any biases and make this more apt to multi-threading
        shuffle(self.state)
        with open("../words.txt", 'r') as f:
            self.words = set(x for x in f.read().lower().split() if len(x) > 2)
            self.words.update(['a', 'i', "of", "to", "in", "it", "is", "be", "as", "at", "so", "we", "he", "by", "or", "on", "do", "if", "me", "my", "up", "an", "go", "no", "us", "am"])


    def move(self):
        '''Gets a single movement away from the current state for the annealling function
        In our case we also check to see if the movement is a word and log it in the set of found words
        if it is one. We're not looking for a global minima, we're looking for lots of low values'''

        # Movement in our case is going to be swapping two random letters
        r = random()
        if r > AnagramSolver.SPACE_FREQUENCY:
            x = randrange(len(self.state))
            y = randrange(len(self.state))
            self.state[x], self.state[y] = self.state[y], self.state[x]
        elif r > AnagramSolver.SPACE_FREQUENCY / 2 and " " in self.state:
            self.state.remove(" ")
        else:
            self.state.insert(randrange(len(self.state)), " ")

        word = tuple(sorted("".join(self.state).split()))
        if all(w in self.words for w in word):
            self.found_words.add(word)

    def energy(self):
        '''Calculates the cost function on a state - how close our model thinks it is to a word.
        The increased length generally punishes longer words, meaning punishing additional spaces'''
        token = self.state
        probability = 0
        for letters in zip(token, token[1:], token[2:]):
            probability += -log(self.model.get_probability(letters))

        return probability
