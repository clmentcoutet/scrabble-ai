from typing import List

from src.utils.grid import WordPlacerChecker
from src.search_strategy.WordSearchStrategy import WordSearchStrategy
from src.utils.typing_utils import PlaceWord


class NaiveSearch(WordSearchStrategy):
    def find_best_word(
        self, rack: List[str], word_placer_checker: WordPlacerChecker
    ) -> PlaceWord:
        raise NotImplementedError("Method find_best_word not implemented")
