from collections import Counter
from typing import List

from src.engine.grid import compute_total_word_score
from src.engine.word_checker import WordPlacerChecker
from src.search_strategy.WordSearchStrategy import WordSearchStrategy
from src.engine.tree import Tree
from src.utils.utils import measure_execution_time, count_letters
from src.utils.logger_config import logger
from src.utils.typing import enum, typed_dict as td
from src.utils.typing.default import DEFAULT_PLACE_WORD


@measure_execution_time
def _find_words(letters: list, tree: Tree) -> List[str]:
    """
    Find all valid words that can be formed with the given letters
    :param letters: list of letters
    :param tree: tree containing all valid words
    :return: list of valid words
    """
    letters_count = count_letters(letters)
    results: List[str] = []
    tree.search(tree.root, letters_count, [], results)
    return sorted(results, key=len, reverse=True)


class UltraNaiveSearch(WordSearchStrategy):
    def find_best_word(
        self, rack: List[str], word_placer_checker: WordPlacerChecker
    ) -> td.ValidWord:
        max_score = 0
        best_word: td.PlaceWord = DEFAULT_PLACE_WORD
        letter_used = []
        list_possible_words = _find_words(rack, word_placer_checker.words_tree)
        logger.debug(f"Possible words: {list_possible_words}")
        for word in list_possible_words:
            for direction in [enum.Direction.HORIZONTAL, enum.Direction.VERTICAL]:
                for row in range(15):
                    for col in range(15):
                        result = word_placer_checker.is_word_placable(
                            word, (row, col), direction
                        )
                        if result["state"]:
                            score = compute_total_word_score(
                                td.PlaceWord(
                                    word=word,
                                    start_position=(row, col),
                                    direction=direction,
                                ),
                                result["perpendicular_words"],
                                len(result["letter_already_placed"]),
                            )
                            if score > max_score:
                                max_score = score
                                best_word = td.PlaceWord(
                                    word=word,
                                    start_position=(row, col),
                                    direction=direction,
                                )
                                logger.info(
                                    f"New best word: {best_word} with score {max_score}"
                                )
                                letter_used = list(
                                    (
                                        Counter(word)
                                        - Counter(result["letter_already_placed"])
                                    ).elements()
                                )
        logger.debug(f"Best word: {best_word}")
        return {
            "play": best_word,
            "letter_used": letter_used,
            "score": max_score,
        }
