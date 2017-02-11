# Dictionary

This works by making dictionaries that map a sorted string to all words containing the same letters as the sorted string. This means it can support constant time anagram solving given knowing all letters in the string. From there, we take in a JSON that contains a list of found targets with all letters that that target could possibly represent, and the maximum number of targets that might not have been found.

The program then creates a generator of all combinations of letters that these targets may represent, then runs through the generator and creates a list of all words that may be created.

TODO: Add support for spaces (i.e. multiple words). Weird because unix dictionary has way too many 1 and 2 letter words - may just hardcode from scrabble dictionary or something I guess.