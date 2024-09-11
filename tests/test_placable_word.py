import pytest
import numpy as np
from typing import List

from src.utils.grid import WordPlacerChecker, Grid
from src.utils.typing_utils import Direction


class MockTree:
    def __init__(self, valid_words: List[str]):
        self.valid_words = set(valid_words)

    def is_word(self, word: str) -> bool:
        return word.lower() in self.valid_words


@pytest.fixture
def empty_grid():
    return Grid(np.full((15, 15), "", dtype=str))


@pytest.fixture
def mock_tree():
    return MockTree(
        ["test", "tout", "atout", "soir", "rat", "ta", "or", "toute", "tester"]
    )


@pytest.fixture
def word_placer(empty_grid, mock_tree):
    return WordPlacerChecker(empty_grid, mock_tree)


def test_is_word_in_bounds(word_placer):
    assert word_placer._is_word_in_bounds((7, 7), "test", Direction.HORIZONTAL)
    assert word_placer._is_word_in_bounds((7, 7), "test", Direction.VERTICAL)
    assert not word_placer._is_word_in_bounds((7, 12), "test", Direction.HORIZONTAL)
    assert not word_placer._is_word_in_bounds((12, 7), "test", Direction.VERTICAL)
    assert not word_placer._is_word_in_bounds(
        (7, 7), "verylongwordthatdoesntfit", Direction.HORIZONTAL
    )


def test_is_grid_empty(word_placer):
    assert word_placer._is_grid_empty()
    word_placer.grid[7, 7] = "A"
    assert not word_placer._is_grid_empty()


def test_check_first_word_placement(word_placer):
    assert word_placer._check_first_word_placement(
        (7, 7), "test", Direction.HORIZONTAL
    )["state"]
    assert word_placer._check_first_word_placement((7, 7), "test", Direction.VERTICAL)[
        "state"
    ]
    assert not word_placer._check_first_word_placement(
        (0, 0), "test", Direction.HORIZONTAL
    )["state"]
    assert not word_placer._check_first_word_placement(
        (14, 14), "test", Direction.VERTICAL
    )["state"]


def test_get_word_part(word_placer):
    word_placer.grid[7, 7:10] = list("tou")
    assert word_placer._get_word_part(7, 10, 0, -1) == "tou"
    assert word_placer._get_word_part(7, 6, 0, 1) == "tou"

    word_placer.grid[7:10, 7] = list("tou")
    assert word_placer._get_word_part(10, 7, -1, 0) == "tou"
    assert word_placer._get_word_part(6, 7, 1, 0) == "tou"


def test_get_vertical_word(word_placer):
    word_placer.grid[6:9, 7] = list("tou")
    assert word_placer._get_vertical_word(9, 7, "e") == "toue"


def test_get_horizontal_word(word_placer):
    word_placer.grid[7, 6:9] = list("tou")
    assert word_placer._get_horizontal_word(7, 9, "e") == "toue"


def test_check_perpendicular_word(word_placer):
    word_placer.grid[7, 7:10] = list("tou")
    assert word_placer._check_perpendicular_word((8, 7), "a", Direction.VERTICAL)[
        "state"
    ]
    assert word_placer._check_perpendicular_word((6, 8), "x", Direction.VERTICAL)[
        "state"
    ]
    assert word_placer._check_perpendicular_word((7, 10), "t", Direction.VERTICAL)[
        "state"
    ]
    assert not word_placer._check_perpendicular_word((7, 10), "x", Direction.VERTICAL)[
        "state"
    ]


def test_check_word_placement(word_placer):
    word_placer.grid[7, 7:11] = list("tout")
    assert word_placer._check_word_placement((6, 7), "atout", Direction.VERTICAL)[
        "state"
    ]
    assert word_placer._check_word_placement((7, 6), "atoute", Direction.HORIZONTAL)[
        "state"
    ]
    assert not word_placer._check_word_placement((6, 7), "axout", Direction.VERTICAL)[
        "state"
    ]


def test_is_word_placable(word_placer):
    # First word placement
    assert word_placer.is_word_placable((7, 7), "test", Direction.HORIZONTAL)["state"]

    # Update grid
    word_placer.grid[7, 7:11] = list("test")
    # Valid placements
    assert word_placer.is_word_placable((7, 7), "tout", Direction.VERTICAL)["state"]
    assert word_placer.is_word_placable((7, 7), "tester", Direction.HORIZONTAL)["state"]

    # Invalid placements
    assert (
        not word_placer.is_word_placable((7, 7), "test", Direction.HORIZONTAL)[
            "letter_already_placed"
        ]
        != []
    )  # Overlapping
    assert not word_placer.is_word_placable((0, 0), "test", Direction.HORIZONTAL)[
        "state"
    ]  # Not touching
    assert not word_placer.is_word_placable((6, 8), "invalid", Direction.VERTICAL)[
        "state"
    ]  # Invalid word


def test_is_word_placable_edge_cases(word_placer):
    # Word too long
    assert not word_placer.is_word_placable((7, 7), "a" * 16, Direction.HORIZONTAL)[
        "state"
    ]

    # Word at edge of grid
    assert word_placer.is_word_placable((14, 7), "test", Direction.HORIZONTAL)["state"]
    assert not word_placer.is_word_placable((14, 7), "test", Direction.VERTICAL)[
        "state"
    ]

    # Word creating invalid perpendicular word
    word_placer.grid[7, 7:11] = list("test")
    assert not word_placer.is_word_placable((6, 8), "ax", Direction.VERTICAL)["state"]


if __name__ == "__main__":
    pytest.main()
