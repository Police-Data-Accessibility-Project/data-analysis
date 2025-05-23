import spacy

SPACY_MODEL = spacy.load('en_core_web_trf')  # Largest, slowest, most accurate model
# SPACY_MODEL = spacy.load('en_core_web_sm') # Smallest, fastest, least accurate model

