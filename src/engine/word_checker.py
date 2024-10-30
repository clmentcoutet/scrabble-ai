from typing import Tuple, List, Dict

import numpy as np

from src.engine.grid import Grid
from src.engine.tree import Tree
from src.settings.logger_config import logger
from src.utils.typing import enum, typed_dict as td


class WordPlacerChecker:
    def __init__(self, grid: Grid, words_tree: Tree):
        self.grid: Grid = grid
        self.tree: Tree = words_tree

    def is_word_placable(
        self, word: str, start_position: Tuple[int, int], direction: enum.Direction
    ) -> td.Result:
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
        if not self._is_word_in_bounds(word, start_position, direction):
            return self._create_result(False, {}, "Word does not fit on the grid")

        place_word = self.get_full_word(word, start_position, direction)

        if not self._is_word_in_bounds(**place_word):
            return self._create_result(False, {}, "Word does not fit on the grid")

        if not self.tree.is_word(place_word["word"]):
            return self._create_result(False, {}, f"Word {word} is not valid")

        if self._is_grid_empty():
            return self._check_first_word_placement(**place_word)

        return self._check_word_placement(**place_word)

    def get_full_word(
        self, word: str, start_position: Tuple[int, int], direction: enum.Direction
    ) -> td.PlaceWord:
        """
        Get the full word to be placed on the grid, including any existing letters it connects to.

        Args:
            word (str): The word we want to place
            start_position (Tuple[int, int]): The starting position (x, y) for word placement
            direction (Direction): The direction (horizontal or vertical) to place the word

        Returns:
            PlaceWord: A PlaceWord object containing:
                - full_word: The complete word including existing letters
                - start_position: The starting position of the complete word
                - direction: The direction of the word
        """
        # Calculate the prefix and suffix
        prefix, new_start_position = self._get_prefix(start_position, direction)
        suffix = self._get_suffix(word, start_position, direction)

        # Combine the prefix, word, and suffix to get the full word
        full_word = prefix + word + suffix

        return td.PlaceWord(
            word=full_word, start_position=new_start_position, direction=direction
        )

    def _get_prefix(
        self, start_position: Tuple[int, int], direction: enum.Direction
    ) -> Tuple[str, Tuple[int, int]]:
        """Helper function to get the prefix before the word based on the direction."""
        y, x = start_position
        prefix = ""
        new_start_position = start_position

        if direction == enum.Direction.HORIZONTAL:
            current_x = x - 1
            while current_x >= 0 and self.grid[y, current_x] != "":
                prefix = self.grid[y, current_x] + prefix
                current_x -= 1
            if prefix:
                new_start_position = (y, current_x + 1)
        else:  # Direction.VERTICAL
            current_y = y - 1
            while current_y >= 0 and self.grid[current_y, x] != "":
                prefix = self.grid[current_y, x] + prefix
                current_y -= 1
            if prefix:
                new_start_position = (current_y + 1, x)

        return prefix, new_start_position

    def _get_suffix(
        self, word: str, start_position: Tuple[int, int], direction: enum.Direction
    ) -> str:
        """Helper function to get the suffix after the word based on the direction."""
        y, x = start_position
        suffix = ""

        if direction == enum.Direction.HORIZONTAL:
            current_x = x + len(word)
            width = self.grid.grid.shape[1]
            while current_x < width and self.grid[y, current_x] != "":
                suffix += self.grid[y, current_x]
                current_x += 1
        else:  # Direction.VERTICAL
            current_y = y + len(word)
            height = self.grid.grid.shape[0]
            while current_y < height and self.grid[current_y, x] != "":
                suffix += self.grid[current_y, x]
                current_y += 1

        return suffix

    @staticmethod
    def _is_word_in_bounds(
        word: str, start_position: Tuple[int, int], direction: enum.Direction
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
        if direction == enum.Direction.HORIZONTAL and y + len(word) >= 15:
            return False
        if direction == enum.Direction.VERTICAL and x + len(word) >= 15:
            return False
        return True

    def _is_grid_empty(self) -> np.bool:
        """
        Check if the grid is empty
        :return:
        """
        return np.all(self.grid.grid == "")

    def _check_first_word_placement(
        self, word: str, start_position: Tuple[int, int], direction: enum.Direction
    ) -> td.Result:
        """
        Check if the first word can be placed on the grid
        :param start_position:
        :param word:
        :param direction:
        :return:
        """
        x, y = start_position
        if direction == enum.Direction.HORIZONTAL:
            if y + len(word) - 1 < 7 or y > 7 or x != 7:
                return self._create_result(
                    False, {}, "First word must pass through the center cell"
                )
        else:
            if x + len(word) - 1 < 7 or x > 7 or y != 7:
                return self._create_result(
                    False, {}, "First word must pass through the center cell"
                )
        return self._create_result(True, {}, "")

    def _check_word_placement(
        self, word: str, start_position: Tuple[int, int], direction: enum.Direction
    ) -> td.Result:
        """
        Check if a word can be placed on the grid
        :param start_position:
        :param word:
        :param direction:
        :return:
        """
        letter_already_placed = {}
        perpendicular_words = []
        is_touching_existing_word = False
        x, y = start_position

        for i, letter in enumerate(word):
            current_pos = (
                (x, y + i) if direction == enum.Direction.HORIZONTAL else (x + i, y)
            )
            grid_letter = self.grid[current_pos]
            if grid_letter != "":
                if grid_letter != letter:
                    return self._create_result(
                        False,
                        {},
                        f"Looking to place letter {letter} at position {current_pos} but found {grid_letter}",
                    )
                else:
                    letter_already_placed[i] = letter
                is_touching_existing_word = True
            else:
                horizontal_result = self._check_perpendicular_word(
                    current_pos, letter, direction
                )
                if not horizontal_result["state"]:
                    return horizontal_result
                is_touching_existing_word = is_touching_existing_word or (
                    horizontal_result["state"]
                    and horizontal_result["perpendicular_words"] != []
                )
                perpendicular_words.extend(horizontal_result["perpendicular_words"])
        if len(letter_already_placed) == len(word):
            return self._create_result(False, {}, "Word is already placed on the grid")

        return self._create_result(
            is_touching_existing_word,
            letter_already_placed,
            "",
            perpendicular_words=perpendicular_words,
        )

    def _check_perpendicular_word(
        self, position: Tuple[int, int], letter: str, direction: enum.Direction
    ) -> td.Result:
        """
        Check if a perpendicular word is valid
        :param position: position of the letter
        :param letter:
        :param direction: direction of the word to be placed
        :return:
        """
        x, y = position
        if direction == enum.Direction.HORIZONTAL:
            top_touching = x - 1 >= 0 and self.grid[x - 1, y] != ""
            bottom_touching = x + 1 < 15 and self.grid[x + 1, y] != ""
            place_word = self._get_vertical_word(x, y, letter)
        else:
            top_touching = y - 1 >= 0 and self.grid[x, y - 1] != ""
            bottom_touching = y + 1 < 15 and self.grid[x, y + 1] != ""
            place_word = self._get_horizontal_word(x, y, letter)

        logger.debug(f"Checking perpendicular word {place_word}")

        if not (top_touching or bottom_touching):
            return self._create_result(True, {}, "", perpendicular_words=[])

        if not self.tree.is_word(place_word["word"]):
            return self._create_result(
                False, {}, f"Word {place_word['word']} is not valid"
            )

        return self._create_result(
            top_touching or bottom_touching,
            {},
            "",
            perpendicular_words=[place_word],
        )

    def _get_vertical_word(self, x: int, y: int, letter: str) -> td.PlaceWord:
        """
        Get the vertical word that contains the letter at position (x, y) and its starting position

        Args:
            x: position x of the letter
            y: position y of the letter
            letter: the letter at position (x, y)

        Returns:
            Tuple containing:
                - str: The complete vertical word
                - Tuple[int, int]: The starting position of the complete word
        """
        up_part, up_pos = self._get_word_part(x, y, -1, 0)
        down_part, _ = self._get_word_part(x, y, 1, 0)

        # The starting position is where the upward search ended
        return {
            "word": up_part + letter + down_part,
            "start_position": up_pos,
            "direction": enum.Direction.VERTICAL,
        }

    def _get_horizontal_word(self, x: int, y: int, letter: str) -> td.PlaceWord:
        """
        Get the horizontal word that contains the letter at position (x, y) and its starting position

        Args:
            x: position x of the letter
            y: position y of the letter
            letter: the letter at position (x, y)

        Returns:
            Tuple containing:
                - str: The complete horizontal word
                - Tuple[int, int]: The starting position of the complete word
        """
        left_part, left_pos = self._get_word_part(x, y, 0, -1)
        right_part, _ = self._get_word_part(x, y, 0, 1)

        # The starting position is where the leftward search ended
        return {
            "word": left_part + letter + right_part,
            "start_position": left_pos,
            "direction": enum.Direction.HORIZONTAL,
        }

    def _get_word_part(
        self, x: int, y: int, dx: int, dy: int
    ) -> Tuple[str, Tuple[int, int]]:
        """
        Get the word part and its starting position in the direction (dx, dy) from position (x, y)

        Args:
            x: Starting x position
            y: Starting y position
            dx: Direction in x (-1, 0, or 1)
            dy: Direction in y (-1, 0, or 1)

        Returns:
            Tuple containing:
                - str: The word part found in the given direction
                - Tuple[int, int]: The starting position of this word part
        """
        word = ""
        nx, ny = x + dx, y + dy

        while 0 <= nx < 15 and 0 <= ny < 15 and self.grid[nx, ny] != "":
            word += self.grid[nx, ny]
            nx, ny = nx + dx, ny + dy

        if dx < 0 or dy < 0:
            # For backward direction, the start position is where we stopped
            start_x, start_y = nx + dx, ny + dy
            word = word[::-1]
        else:
            # For forward direction, the start position is where we started looking
            start_x, start_y = x + dx, y + dy

        return word, (start_x, start_y)

    @staticmethod
    def _create_result(
        state: bool,
        letter_already_placed: Dict[int, str],
        message: str,
        perpendicular_words: List[td.PlaceWord] | None = None,
    ) -> td.Result:
        """
        Create a result dictionary
        :param state:
        :param letter_already_placed:
        :param message:
        :param perpendicular_words:
        :return:
        """
        if perpendicular_words is None:
            perpendicular_words = []
        return {
            "state": state,
            "letter_already_placed": letter_already_placed,
            "message": message,
            "perpendicular_words": perpendicular_words,
        }
