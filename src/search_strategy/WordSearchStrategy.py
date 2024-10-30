from typing import List, Dict, Optional

from src.engine.tree import Tree
from src.engine.word_checker import WordPlacerChecker
from src.utils.typing import typed_dict as td
from src.utils.utils import count_letters


class WordSearchStrategy:
    def __init__(self):
        self.strategy_code = "base"

    @staticmethod
    def _find_all_possible_word(
        rack: List[str], tree: Tree, constraint: Optional[Dict[int, str]] = None
    ) -> List[str]:
        """
        Find all valid words that can be formed with the given letters
        :param rack: list of letters
        :param tree: tree containing all valid words
        :param constraint: constraint on the words, e.g. the word must contain the letter at index 0
        :return: list of valid words
        """
        letters_count = count_letters(rack)
        results: List[str] = []
        tree.search(tree.root, letters_count, [], results, constraint=constraint)
        return results

    def find_best_word(
        self, rack: List[str], word_placer_checker: WordPlacerChecker, score_grid
    ) -> td.ValidWord:
        raise NotImplementedError("Subclasses must implement this method")
