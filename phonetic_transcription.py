import sys
import os
import argparse
import simpleaudio
import nltk
import string
import numpy
import nltk
import inflect
import td_psola 

# Sample rate constant
RATE = 8000

class Phonetic_Transcription:

    def __init__(self, diphones, directory, phrases):
        """
        Initialize synthesizer.
        - `diphones` (list): sequence of diphones
        - `audio` (dict): dictionary of filename-audio pairs
        """
        self.diphones = diphones
        # Initialize token filter and pronunciation lexicon
        self.filter = set(string.punctuation)       #creates a list of symbols that will be removed later
        self.lexicon = nltk.corpus.cmudict.dict() 
        
        
        # Accessing the phrases
        for subtree in phrases.subtrees():
            f_0 = 0.8
            if subtree.label() is not None and subtree.label() != 'S':  # Ignore the main sentence structure
                # Tokenize and extract phones from input utterance
                phones = []
                for leaf in subtree.leaves(): 
                    for phone in self.get_phones(leaf):
                            phones.append(phone) #creates a list of phones from the words tokenized
                    
                self.diphones = self.get_diphones(phones)
                
                # Create mapping from diphone filenames to audio
                audio = {}
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
                        output = self.get_audio(audio)
                        # Define segment start and end indices (adjust as needed)
                        N=len(output)
                        segment_starts = [0, int(N/3), int(2*N/3)]  # Example: Divide into three equal parts
                        segment_ends = [int(N/3), int(2*N/3), N]
                         # Define pitch shift ratios for each segment
                        f_ratio_values = [1.0, 0.7, 0.3]  # Adjust as needed
                        for i, (start, end) in enumerate(zip(segment_starts, segment_ends)):
                             
                            # Extract segment
                            segment = output[start:end]

                            # Choose the corresponding pitch shift ratio for the segment
                            f_ratio = f_ratio_values[i]

                            # Shift pitch for the segment
                            new_segment = td_psola.shift_pitch(segment, RATE, f_ratio)

                            # Replace the original segment with the pitch-shifted segment
                            output[start:end] = new_segment
                        
                        
                       
            else:
               # Tokenize and extract phones from input utterance
                phones = []
                for leaf in subtree.leaves(): 
                    for phone in self.get_phones(leaf):
                            phones.append(phone) #creates a list of phones from the words tokenized
                    
                self.diphones = self.get_diphones(phones)
                
                # Create mapping from diphone filenames to audio
                audio = {}
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
                        output = self.get_audio(audio)
                        # Define segment start and end indices (adjust as needed)
                        N=len(output)
                        segment_starts = [0, int(N/3), int(2*N/3)]  # Example: Divide into three equal parts
                        segment_ends = [int(N/3), int(2*N/3), N]
                         # Define pitch shift ratios for each segment
                        f_ratio_values = [1.0, 0.7, 0.3]  # Adjust as needed
                        for i, (start, end) in enumerate(zip(segment_starts, segment_ends)):
                             
                            # Extract segment
                            segment = output[start:end]

                            # Choose the corresponding pitch shift ratio for the segment
                            f_ratio = f_ratio_values[i]

                            # Shift pitch for the segment
                            new_segment = td_psola.shift_pitch(segment, RATE, f_ratio)

                            # Replace the original segment with the pitch-shifted segment
                            output[start:end] = new_segment
    
    
    
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

                
    def get_diphones(self, phones):
        """
        Expand phone sequence into a diphone sequence. 
        """
        # Initialize diphone sequence
        diphones = [[None, phones[0]]]

        # Expand phones into diphones
        for i in range(len(phones) - 1): #puts 2 consecutive phones into one element as a diphone
            ph1 = phones[i]
            ph2 = phones[i + 1]
            diphones.append([ph1, ph2])

        # Add last diphone to sequence
        diphones.append([phones[len(phones) - 1], None])
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
        output.data = numpy.concatenate(output_audio)
        output.rescale(1.0)
        return output