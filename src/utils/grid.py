from typing import List, Tuple, Dict

import numpy as np

from src import settings
from src.utils import utils
from src.utils.logger_config import logger
from src.utils.tree import Tree
from src.utils.typing_utils import CellValue, Direction, Result, PlaceWord

LETTER_VALUES = utils.load_letter_values(settings.LETTERS_VALUES_PATH)


def compute_score(
    word: str,
    start_position: tuple,
    direction: Direction,
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
    for i, letter in enumerate(word):
        x, y = start_position
        if direction == Direction.HORIZONTAL:
            x += i
        else:
            y += i
        cell_value = SCORE_GRID[x, y]
        letter_value = LETTER_VALUES[letter]["value"]
        match cell_value:
            case CellValue.EMPTY.value:
                score += letter_value
            case CellValue.DOUBLE_WORD.value:
                score += letter_value
                word_multiplier *= 2
            case CellValue.TRIPLE_WORD.value:
                score += letter_value
                word_multiplier *= 3
            case CellValue.DOUBLE_LETTER.value:
                score += letter_value * 2
            case CellValue.TRIPLE_LETTER.value:
                score += letter_value * 3
            case CellValue.START.value:
                SCORE_GRID[x, y] = 0
                score += letter_value
                word_multiplier *= 2
    return score * word_multiplier


class Grid:
    def __init__(self, grid: np.ndarray = np.zeros((15, 15), dtype=str)):
        self.grid = grid

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
        self, word: str, start_position: tuple, direction: Direction
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
            if direction == Direction.HORIZONTAL:
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


def compute_total_word_score(
    place_word: PlaceWord, perpendicular_words: Dict[str, str]
) -> int:
    """
    Compute the total score of a word placed on the grid
    :param place_word:
    :param perpendicular_words:
    :return:
    """
    word = place_word["word"]
    row, column = place_word["start_position"]
    direction = place_word["direction"]
    logger.debug(f"Placing word {word} at position {row, column} in direction {direction}")
    score = compute_score(word, (column, row), direction)
    for letter, perpendicular_word in perpendicular_words.items():
        perpendicular_score = compute_score(
            perpendicular_word,
            (row, column),
            Direction.VERTICAL
            if direction == Direction.HORIZONTAL
            else Direction.HORIZONTAL,
        )
        score += perpendicular_score
    return score


class WordPlacerChecker:
    def __init__(self, grid: Grid, words_tree: Tree):
        self.grid: Grid = grid
        self.words_tree: Tree = words_tree

    def is_word_placable(
        self, word: str, start_position: Tuple[int, int], direction: Direction
    ) -> Result:
        """
        Check if a word can be placed on the grid.
        A word can be placed if:
            - it fits on the grid
            - it is adjacent to an existing word
            - place the word does not create an invalid word
        :param start_position:
        :param word:
        :param direction:
        :return: Tuple of boolean and list of needed letters to place the chosen word
        :rtype: object

        """
        if not self.words_tree.is_word(word):
            return self._create_result(False, [], f"Word {word} is not valid")

        if not self._is_word_in_bounds(word, start_position, direction):
            return self._create_result(False, [], "Word does not fit on the grid")

        if self._is_grid_empty():
            return self._check_first_word_placement(word, start_position, direction)

        return self._check_word_placement(word, start_position, direction)

    @staticmethod
    def _is_word_in_bounds(
        word: str, start_position: Tuple[int, int], direction: Direction
    ) -> bool:
        """
        Check if a word is in bounds of the grid
        :param start_position:
        :param word:
        :param direction:
        :return:
        """
        x, y = start_position
        if len(word) > 15:
            return False
        if direction == Direction.HORIZONTAL and y + len(word) > 15:
            return False
        if direction == Direction.VERTICAL and x + len(word) > 15:
            return False
        return True

    def _is_grid_empty(self) -> np.bool:
        """
        Check if the grid is empty
        :return:
        """
        return np.all(self.grid.grid == "")

    def _check_first_word_placement(
        self, word: str, start_position: Tuple[int, int], direction: Direction
    ) -> Result:
        """
        Check if the first word can be placed on the grid
        :param start_position:
        :param word:
        :param direction:
        :return:
        """
        x, y = start_position
        if direction == Direction.HORIZONTAL:
            if y + len(word) - 1 < 7 or y > 7 or x != 7:
                return self._create_result(
                    False, [], "First word must pass through the center cell"
                )
        else:
            if x + len(word) - 1 < 7 or x > 7 or y != 7:
                return self._create_result(
                    False, [], "First word must pass through the center cell"
                )
        return self._create_result(True, [], "")

    def _check_word_placement(
        self, word: str, start_position: Tuple[int, int], direction: Direction
    ) -> Result:
        """
        Check if a word can be placed on the grid
        :param start_position:
        :param word:
        :param direction:
        :return:
        """
        letter_already_placed = []
        perpendicular_words = {}
        is_touching_existing_word = False
        x, y = start_position

        for i, letter in enumerate(word):
            current_pos = (
                (x, y + i) if direction == Direction.HORIZONTAL else (x + i, y)
            )
            grid_letter = self.grid[current_pos]
            if grid_letter != "":
                if grid_letter != letter:
                    return self._create_result(
                        False,
                        [],
                        f"Looking to place letter {letter} at position {current_pos} but found {grid_letter}",
                    )
                else:
                    letter_already_placed.append(letter)
                is_touching_existing_word = True
            else:
                horizontal_result = self._check_perpendicular_word(
                    current_pos, letter, direction
                )
                if not horizontal_result["state"]:
                    return horizontal_result
                is_touching_existing_word = is_touching_existing_word or (
                    horizontal_result["state"]
                    and horizontal_result["perpendicular_words"] != {}
                )
                perpendicular_words.update(horizontal_result["perpendicular_words"])

        return self._create_result(
            is_touching_existing_word,
            letter_already_placed,
            "",
            perpendicular_words=perpendicular_words,
        )

    def _check_perpendicular_word(
        self, position: Tuple[int, int], letter: str, direction: Direction
    ) -> Result:
        """
        Check if a perpendicular word is valid
        :param position: position of the letter
        :param letter:
        :param direction: direction of the word to be placed
        :return:
        """
        x, y = position
        if direction == Direction.HORIZONTAL:
            top_touching = x - 1 >= 0 and self.grid[x - 1, y] != ""
            bottom_touching = x + 1 < 15 and self.grid[x + 1, y] != ""
            vertical_word = self._get_vertical_word(x, y, letter)
        else:
            top_touching = y - 1 >= 0 and self.grid[x, y - 1] != ""
            bottom_touching = y + 1 < 15 and self.grid[x, y + 1] != ""
            vertical_word = self._get_horizontal_word(x, y, letter)

        if not (top_touching or bottom_touching):
            return self._create_result(True, [], "", perpendicular_words={})

        if not self.words_tree.is_word(vertical_word):
            return self._create_result(False, [], f"Word {vertical_word} is not valid")

        return self._create_result(
            top_touching or bottom_touching,
            [],
            "",
            perpendicular_words={letter: vertical_word},
        )

    def _get_vertical_word(self, x: int, y: int, letter: str) -> str:
        """
        Get the vertical word that contains the letter at position (x, y)
        :param x: position x of the letter
        :param y: position y of the letter
        :param letter:
        :return:
        """
        return (
            self._get_word_part(x, y, -1, 0) + letter + self._get_word_part(x, y, 1, 15)
        )

    def _get_horizontal_word(self, x: int, y: int, letter: str) -> str:
        """
        Get the horizontal word that contains the letter at position (x, y)
        :param x:
        :param y:
        :param letter:
        :return:
        """
        return (
            self._get_word_part(x, y, 0, -1) + letter + self._get_word_part(x, y, 0, 1)
        )

    def _get_word_part(self, x: int, y: int, dx: int, dy: int) -> str:
        """
        Get the word part in the direction (dx, dy) from position (x, y)
        :param x:
        :param y:
        :param dx:
        :param dy:
        :return:
        """
        word = ""
        nx, ny = x + dx, y + dy
        while 0 <= nx < 15 and 0 <= ny < 15 and self.grid[nx, ny] != "":
            word += self.grid[nx, ny]
            nx, ny = nx + dx, ny + dy
        return word[::-1] if dx < 0 or dy < 0 else word

    @staticmethod
    def _create_result(
        state: bool,
        letter_already_placed: List[str],
        message: str,
        perpendicular_words: Dict[str, str] | None = None,
    ) -> Result:
        """
        Create a result dictionary
        :param state:
        :param letter_already_placed:
        :param message:
        :param perpendicular_word:
        :return:
        """
        if perpendicular_words is None:
            perpendicular_words = {}
        return {
            "state": state,
            "letter_already_placed": letter_already_placed,
            "message": message,
            "perpendicular_words": perpendicular_words,
        }
