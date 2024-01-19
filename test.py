# Assuming both classes are in separate files or in the same file

# Importing the classes
from linguistic_analysis import Linguistic_Analysis
from pre_processing import Pre_Processing
from phonetic_transcription import Phonetic_Transcription

# Test input
input_text = "This film is coming to the cinemas in a date TBA."

# Test Pre-Processing
pre_processing_instance = Pre_Processing(input_text)

print("\nPre-Processing Output:")
print("Input Text:", input_text)
print("Output Text:", pre_processing_instance.output_text)

# Test Linguistic Analysis
linguistic_analysis_instance = Linguistic_Analysis(pre_processing_instance.output_text)
pos_tags = linguistic_analysis_instance.disambiguate_pos(pre_processing_instance.output_text)
phrases = linguistic_analysis_instance.syntatic_analysis(pos_tags, pre_processing_instance.output_text )

print("\nLinguistic Analysis Output:")
print("Input Text:", input_text)
print("POS Tags:", pos_tags)
print("Phrases:", phrases)

phonetic_transcription_instance = Phonetic_Transcription("./diphones", pre_processing_instance.output_text)
