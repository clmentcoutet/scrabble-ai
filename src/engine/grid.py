from typing import List

import numpy as np

from src import settings
from src.utils import utils
from src.utils.logger_config import logger
from src.utils.typing import enum, typed_dict as td

LETTER_VALUES = utils.load_letter_values(settings.LETTERS_VALUES_PATH)


class Grid:
    def __init__(self, grid: np.ndarray = None):
        if grid is None:
            self.grid = np.array([[""] * 15] * 15, dtype=str)
        else:
            # Create a deep copy of the input grid to ensure independence
            self.grid = np.array(grid, copy=True)

    def __getitem__(self, item):
        return self.grid[item]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            expected_shape = self.grid[key].shape
            value = np.array(value)
            if value.ndim == 1 and len(expected_shape) == 2:
                value = value.reshape(expected_shape)

        self.grid[key] = value

    def __str__(self):
        # print number 1 to 15
        result = "   " + "  ".join([f"{i:2}" for i in range(0, 15)]) + "\n"
        result += f"  |{'|'.join(['---'] * 15)}|\n"
        for i, row in enumerate(self.grid):
            result += f"{i:2}|"
            for j, cell in enumerate(row):
                result += "{:^3}|".format(cell)
            result += f"\n  |{'|'.join(['---'] * 15)}|\n"
        return result

    def serialize(self) -> dict:
        return {"grid": self.grid.tolist(), "shape": self.grid.shape}

    def place_word(
        self, word: str, start_position: tuple, direction: enum.Direction
    ) -> None:
        """
        Place a word on the grid
        :param start_position:
        :param word:
        :param direction:
        :return: None
        """
        x, y = start_position
        for i, letter in enumerate(word):
            if direction == enum.Direction.HORIZONTAL:
                self.grid[x, y + i] = letter
            else:
                self.grid[x + i, y] = letter


SCORE_GRID = Grid(
    np.array(
        [
            [4, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 4],
            [0, 1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 3, 0, 3, 0, 0, 0, 1, 0, 0],
            [3, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 3],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0],
            [0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0, 0, 3, 0, 0],
            [4, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0, 3, 0, 0, 4],
            [0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0, 0, 3, 0, 0],
            [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [3, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 3],
            [0, 0, 1, 0, 0, 0, 3, 0, 3, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1, 0],
            [4, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 3, 0, 0, 4],
        ]
    )
)

EMPTY_GRID = Grid(np.array([[""] * 15] * 15))


def _compute_score(
    word: str,
    start_position: tuple,
    direction: enum.Direction,
) -> int:
    """
    Compute the score of a word placed on the grid
    :param start_position:
    :param word:
    :param direction:
    :return:
    """
    score = 0
    word_multiplier = 1
    logger.debug(f"Computing score for word {word}")
    for i, letter in enumerate(word):
        x, y = start_position
        if direction == enum.Direction.HORIZONTAL:
            x += i
        else:
            y += i
        logger.debug(f"Letter {letter} at position {x, y}")
        cell_value = SCORE_GRID[x, y]
        letter_value = LETTER_VALUES[letter]["value"]
        match cell_value:
            case enum.CellValue.EMPTY.value:
                score += letter_value
            case enum.CellValue.DOUBLE_WORD.value:
                score += letter_value
                word_multiplier *= 2
            case enum.CellValue.TRIPLE_WORD.value:
                score += letter_value
                word_multiplier *= 3
            case enum.CellValue.DOUBLE_LETTER.value:
                score += letter_value * 2
            case enum.CellValue.TRIPLE_LETTER.value:
                score += letter_value * 3
            case enum.CellValue.START.value:
                SCORE_GRID[x, y] = 0
                score += letter_value
                word_multiplier *= 2
    return score * word_multiplier


def compute_total_word_score(
    place_word: td.PlaceWord,
    perpendicular_words: List[td.PlaceWord],
    nb_letter_already_placed: int,
) -> int:
    """
    Compute the total score of a word placed on the grid
    :param nb_letter_already_placed:
    :param place_word:
    :param perpendicular_words:
    :return:
    """
    word = place_word["word"]
    row, column = place_word["start_position"]
    direction = place_word["direction"]
    score = _compute_score(word, (column, row), direction)
    if len(word) - nb_letter_already_placed == 7:
        score += 50
    for perpendicular_word in perpendicular_words:
        perpendicular_score = _compute_score(
            perpendicular_word["word"],
            (
                perpendicular_word["start_position"][1],
                perpendicular_word["start_position"][0],
            ),
            perpendicular_word["direction"],
        )
        score += perpendicular_score
    return score
