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
from nltk import RegexpParser

# Sample rate constant
RATE = 16000

class Linguistic_Analysis:
    
    def __init__(self, input_text):
        self.input_text = input_text
        #self.filter = set(string.punctuation)
        #self.lexicon = nltk.corpus.cmudict.dict()
        self.output_text = []

    def disambiguate_pos(self, words):
        # Tokenize the input words
        tokens = nltk.word_tokenize(' '.join(words))

        # Perform POS tagging
        pos_tags = nltk.pos_tag(tokens)

        return pos_tags

    def syntatic_analysis(self, pos_tags, input_text):
        grammar = """ NP: {<DT>?<JJ>*<NN>}
                    P: {<IN>}
                    V: {<V.*>}
                     PP: {<p> <NP>}
                    VP: {<TO>?<V> <NP|PP>*}"""
        parser = RegexpParser(grammar)
        phrases = parser.parse(pos_tags)
        return phrases
    
  





