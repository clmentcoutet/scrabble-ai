from collections import Counter
from typing import List

from src.engine.grid import compute_total_word_score, Grid
from src.engine.word_checker import WordPlacerChecker
from src.search_strategy.WordSearchStrategy import WordSearchStrategy
from src.settings.logger_config import logger
from src.utils.typing import enum, typed_dict as td
from src.utils.typing.default import DEFAULT_PLACE_WORD


class NaiveBlindSearch(WordSearchStrategy):
    """
    UltraNaiveSearch is a search strategy that finds the best word to play by
    checking all possible words that can be formed with the given rack and
    placing them on the board to find the best word to play. This strategy
    does not take into account the board state or the words already placed on
    """

    def __init__(self):
        super().__init__()
        self.strategy_code = "naive_blind"

    def find_best_word(
        self, rack: List[str], word_placer_checker: WordPlacerChecker, score_grid: Grid
    ) -> td.ValidWord:
        max_score = 0
        best_word: td.PlaceWord = DEFAULT_PLACE_WORD
        letter_used = []
        list_possible_words = self._find_all_possible_word(
            rack, word_placer_checker.tree
        )
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
                                len(list(result["letter_already_placed"].values())),
                                score_grid,
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
                                        - Counter(
                                            list(
                                                result["letter_already_placed"].values()
                                            )
                                        )
                                    ).elements()
                                )
        logger.debug(f"Best word: {best_word}")
        return {
            "play": best_word,
            "letter_used": letter_used,
            "score": max_score,
        }
