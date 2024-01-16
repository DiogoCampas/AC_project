import sys
import os
import argparse
import simpleaudio
import nltk
import string
import numpy
import nltk
import inflect
nltk.download('cmudict')
nltk.download('punkt')

# Sample rate constant
RATE = 16000

class Pre_Processing:
    
    
    def __init__(self, input_text):
        
        """
        Initialize pre-processing.
        - `filter` (set): punctuation to be removed from the utterance.
        - `lexicon` (dict): pronunciation lexicon (CMUdict).
        - `utterance` (str): input text.
        - `phones` (list): utterance phonemes.
        """ 
        
        
    