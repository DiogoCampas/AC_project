import sys
import os
import argparse
import simpleaudio
import nltk
import string
import numpy as np
import nltk
import inflect
import td_psola 

# Sample rate constant
RATE = 16000

class Phonetic_Transcription:

    def __init__(self, directory, words):
        """
        Initialize synthesizer.
        - `diphones` (list): sequence of diphones
        - `audio` (dict): dictionary of filename-audio pairs
        """
       
        # Initialize token filter and pronunciation lexicon
        self.filter = set(string.punctuation)       #creates a list of symbols that will be removed later
        self.lexicon = nltk.corpus.cmudict.dict()         
        self.audio = {}
        self.phones = []
        
        for word in words:
            print(word)
            if word in string.punctuation:
                continue
            else:
                for phone in self.get_phones(word):
                        self.phones.append(phone) #creates a list of phones from the words tokenized

        diphones = self.get_diphones()
        
        self.diphones = diphones

        # Create mapping from diphone filenames to audio
        self.audio = {}
        for diphone in self.diphones:
            filename = self.get_filename(diphone)
            if filename not in self.audio:

                # Ensure that file exists
                path = os.path.join(directory, filename)
                if not os.path.isfile(path):
                    sys.exit(f"Couldn't locate '{filename}'")

                # Load its contents and add to dictionary
                audio = simpleaudio.Audio()
                audio.load(path)
                self.audio[filename] = audio
        
        output = self.get_audio()
        output.play()
        output.save("test.wav")
                        
                        
    def get_phones(self, word, variant=0):
        """
        Given a word, return a normalized phonemic transcription
        if available in pronunciation lexicon. Otherwise, exit
        program.
        """
        if word not in self.lexicon:
            sys.exit(f"Couldn't transcribe '{word}'")
            
        # Select variant pronunciation if it exists
        lex_entry = self.lexicon[word] #list of possible pronounciations
        print(lex_entry)
        if variant <= len(lex_entry) - 1:
            pronunciation = lex_entry[variant]
        else:
            pronunciation = lex_entry[0]
    
        return map(lambda phone: phone.lower().rstrip("012"), pronunciation) #transforms to lower case and removes numbers from phoneme and adds the pronounciation selected

                
    def get_diphones(self):
        """
        Expand phone sequence into a diphone sequence. 
        """
        # Initialize diphone sequence
        diphones = [[None, self.phones[0]]]

        # Expand phones into diphones
        for i in range(len(self.phones) - 1): #puts 2 consecutive phones into one element as a diphone
            ph1 = self.phones[i]
            ph2 = self.phones[i + 1]
            diphones.append([ph1, ph2])

        # Add last diphone to sequence
        diphones.append([self.phones[len(self.phones) - 1], None])
        return diphones

    def get_filename(self, diphone):
        """
        Given a diphone, return its corresponding filename.
        """
        ph1 = diphone[0] if diphone[0] is not None else "pau"
        ph2 = diphone[1] if diphone[1] is not None else "pau"
        return f"{ph1}-{ph2}.wav"

    def get_audio(self, rate=RATE):
        """
        Return synthesized output as an `Audio` object containing
        the concatenated audio for the input diphone sequence.
        """
        # Create audio sequence from diphones
        output_audio = []
        for diphone in self.diphones:
            #print(diphone)
            filename = self.get_filename(diphone)
            audio = self.audio[filename]
            output_audio.append(audio.data)

        # Instantiate output `Audio` object
        output = simpleaudio.Audio(rate=rate)

        # Concatenate audio and rescale
        output.data = np.concatenate(output_audio)
        output.rescale(1.0)
        return output