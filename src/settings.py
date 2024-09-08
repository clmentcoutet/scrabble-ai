import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FOLDER = 'data/'
FRENCH_DICTIONARY = 'french.dic'
LETTERS_VALUES = 'french.let'

FRENCH_DICTIONARY_PATH = os.path.join(BASE_DIR, DATA_FOLDER, FRENCH_DICTIONARY)
LETTERS_VALUES_PATH = os.path.join(BASE_DIR, DATA_FOLDER, LETTERS_VALUES)
