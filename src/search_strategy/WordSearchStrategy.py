from typing import List

from src.utils.grid import WordPlacerChecker
from src.utils.typing_utils import PlaceWord, ValidWord


class WordSearchStrategy:
    def __init__(self):
        pass

    def find_best_word(
        self, rack: List[str], word_placer_checker: WordPlacerChecker
    ) -> ValidWord:
        raise NotImplementedError("Subclasses must implement this method")
