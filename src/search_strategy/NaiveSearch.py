from collections import Counter
from typing import List, Tuple, Dict

from src.engine.grid import Grid, compute_total_word_score
from src.engine.word_checker import WordPlacerChecker
from src.search_strategy.WordSearchStrategy import WordSearchStrategy
from src.settings.logger_config import logger
from src.utils.typing import typed_dict as td, enum
from src.utils.typing.default import DEFAULT_PLACE_WORD


class NaiveSearch(WordSearchStrategy):
    """
    UltraNaiveSearch is a search strategy that finds the best word to play by
    checking all possible words that can be formed with the given rack and
    already placed words on the board to find the best word to play.
    """

    def __init__(self):
        super().__init__()
        self.strategy_code = "naive"

    @staticmethod
    def _get_already_place_letters(
        grid: Grid, start_position: Tuple[int, int], direction: enum.Direction
    ) -> Dict[int, str]:
        """
        Get the letters already placed on the board
        :param grid: the grid
        :param start_position: the start position of the word
        :param direction: the direction of the word
        :return: a dictionary mapping positions to letters
        """
        already_place_letters = {}
        if direction == enum.Direction.HORIZONTAL:
            row, col = start_position
            for i in range(col, 15):
                if grid[row, i] != "":
                    already_place_letters[i - col] = str(grid[row, i])
        else:
            row, col = start_position
            for i in range(row, 15):
                if grid[i, col] != "":
                    already_place_letters[i - row] = str(grid[i, col])
        return already_place_letters

    def find_best_word(
        self, rack: List[str], word_placer_checker: WordPlacerChecker, score_grid: Grid
    ) -> td.ValidWord:
        max_score = 0
        best_word: td.PlaceWord = DEFAULT_PLACE_WORD
        letter_used = []
        for direction in [enum.Direction.HORIZONTAL, enum.Direction.VERTICAL]:
            for row in range(15):
                for col in range(15):
                    start_position = (row, col)
                    constraint = self._get_already_place_letters(
                        word_placer_checker.grid, start_position, direction
                    )
                    new_rack = rack.copy()
                    new_rack += list(constraint.values())
                    possible_words = self._find_all_possible_word(
                        new_rack, word_placer_checker.tree, constraint
                    )
                    for word in possible_words:
                        result = word_placer_checker.is_word_placable(
                            word, start_position, direction
                        )
                        # for index, letter in result["letter_already_placed"].items():
                        #    word = word[:index] + letter + word[index + 1 :]
                        if result["state"]:
                            score = compute_total_word_score(
                                td.PlaceWord(
                                    word=word,
                                    start_position=(row, col),
                                    direction=direction,
                                ),
                                result["perpendicular_words"],
                                len(result["letter_already_placed"]),
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
                                logger.info(f"constraint: {constraint}")
                                logger.info(f"result: {result}")
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
