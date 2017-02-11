from __future__ import division
from simanneal import Annealer
from random import shuffle, randrange, random

class AnagramSolver(Annealer):

    SPACE_FREQUENCY = .05

    def __init__(self, model, letters, found_words):
        # This way we can take in basically any iterable
        self.state = list(letters)
        self.num_letters = len(self.state)
        self.model = model
        self.found_words = found_words
        # Start from a random position to remove any biases and make this more apt to multi-threading
        shuffle(self.state)
        with open("/usr/share/dict/words", 'r') as f:
            self.words = set(f.read().lower().split())


    def move(self):
        '''Gets a single movement away from the current state for the annealling function
        In our case we also check to see if the movement is a word and log it in the set of found words
        if it is one. We're not looking for a global minima, we're looking for lots of low values'''

        # Movement in our case is going to be swapping two random letters
        if random() > AnagramSolver.SPACE_FREQUENCY * ((self.num_letters - self.state.count(" "))/len(self.state)):
            x = randrange(len(self.state))
            y = randrange(len(self.state))
            self.state[x], self.state[y] = self.state[y], self.state[x]
        else:
            self.state.insert(randrange(len(self.state)), " ")

        word = "".join(self.state)
        if all(w in self.words for w in word.split()):
            self.found_words.add(word)

    def energy(self):
        '''Calculates the cost function on a state - how close our model thinks it is to a word. We
        do 1 - probability because we're doing minimization'''
        token = self.state
        probability = 0
        for letters in zip(token, token[1:], token[2:]):
            probability += self.model.get_probability(letters)
        probability = probability/len(self.state)

        return (1/probability)