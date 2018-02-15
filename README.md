# CUAir Anagram Solving

One of CUAir's tasks is to identify targets on the ground with letters inscribed in them. These targets make up an anagram that can be solved for extra points. However, our system is not perfect - we may miss targets, and we may misidentify targets that we do see.

This repository consists of two attempts to solve the problem - the somewhat useless overkill (simulated annealling) and the practical (brute force w/ dictionaries).

words.txt contains the most common 10,000 words in American English (http://norvig.com/ngrams/count_1w.txt)