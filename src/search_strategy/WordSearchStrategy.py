from typing import List

from src.engine.word_checker import WordPlacerChecker
from src.utils.typing import typed_dict as td


class WordSearchStrategy:
    def __init__(self):
        pass

    def find_best_word(
        self, rack: List[str], word_placer_checker: WordPlacerChecker
    ) -> td.ValidWord:
        raise NotImplementedError("Subclasses must implement this method")
