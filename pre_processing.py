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

        """ 
        self.input_text = input_text
        self.filter = set(string.punctuation)
        self.output_text = []
        
        
        
        self.output_text = self.get_words(input_text)
        
    
    
    def get_words(self, utterance):
        """
        Return tokenized utterance without punctuation.
        """
        words = []
        for word in nltk.word_tokenize(utterance):
            print(word)

            # Exclude words in filter
            if word in self.filter:
                words.append(word)
            
            if word.isdigit():
                words.append(self.convert_numbers_to_text(word.lower()))

            else:
                words.append(self.convert_abbr_to_text(word.lower()))

        return words

        
    def convert_numbers_to_text(self, text):
            
        p = inflect.engine()
        words = text.split()

        for i, word in enumerate(words):
            if word.isdigit():
                # Convert numerical numbers to text
                words[i] = p.number_to_words(word)

            # Join the words back into a sentence
            return ' '.join(words)
    
    def convert_abbr_to_text(self, text):
        
        words = text.split()

        for i, word in enumerate(words):
            # Check if the word is an abbreviation
            if word.upper() in abbreviation_mapping:
                # Replace the abbreviation with its full form
                words[i] = abbreviation_mapping[word.upper()]

        # Join the words back into a sentence
        expanded_text = ' '.join(words)
        return expanded_text


abbreviation_mapping = {
    "AFAIK" : "As Far As I Know",
    "BRB" : "Be Right Back",
    "BTW" : "By The Way",
    "DIY" : "Do It Yourself",
    "FYI" : "For Your Information",
    "OMG" : "Oh My God",
    "TBA" : "To Be Announced",
    "TBC" : "To Be Continued",
    "TTYL" : "Talk To You Later",
    "WIP" : "Work In Progress",
}

input = "I had lunch, yesterday. OMG I ate 50 pounds of meat!"

# Create an instance of the Pre_Processing class
preprocessor = Pre_Processing(input)

# Access the processed text
processed_text = preprocessor.output_text

# Print the processed text
print("Original Text:")
print(input)
print("\nProcessed Text:")
print(processed_text)

        

        
        
    