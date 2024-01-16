import sys
import os
import argparse
import simpleaudio
import nltk
import string
import numpy
import inflect
from nltk.corpus import wordnet 
nltk.download('cmudict')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Sample rate constant
RATE = 16000

class Linguistic_Analysis:
    
    def __init__(self, input_text):
        self.input_text = input_text
        self.filter = set(string.punctuation)
        self.lexicon = nltk.corpus.cmudict.dict()
        self.output_text = []

    def disambiguate_pos(self, words):
        # Tokenize the input words
        tokens = nltk.word_tokenize(' '.join(words))

        # Perform POS tagging
        pos_tags = nltk.pos_tag(tokens)

        return pos_tags
    
    def choose_best_pronunciation(self, word, pos):
        # Check if the word is in WordNet
        synsets = list(wordnet.synsets(word, pos=wordnet.VERB))  # Example for verbs, adjust as needed
        if synsets:
            # Get all possible pronunciations for the word
            pronunciations = self.lexicon.get(word.lower(), [])
            
        
            # Choose the best pronunciation based on your criteria
            if pronunciations:
                best_pronunciation = pronunciations[0]
                return best_pronunciation

        # Handle the case when the word is not in WordNet or the lexicon
        return None
    

    

# Example usage:
word_list = ["the", "baby", "drinks", "water", "and", "the" , "squirrels", "read", "the", "table"]

linguistic_analysis_instance = Linguistic_Analysis(input_text="")
pos_tags = linguistic_analysis_instance.disambiguate_pos(word_list)

print(pos_tags)



