import pytest
import numpy as np
from typing import List

from src.engine.grid import Grid, _compute_score
from src.engine.word_checker import WordPlacerChecker
from src.utils.typing import enum


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


def test_compute_score():
    assert _compute_score("test", (7, 7), enum.Direction.HORIZONTAL) == 8
    assert _compute_score("toute", (7, 7), enum.Direction.VERTICAL) == 12
    assert _compute_score("tester", (7, 7), enum.Direction.HORIZONTAL) == 14
    assert _compute_score("atout", (7, 7), enum.Direction.VERTICAL) == 12


def test_is_word_in_bounds(word_placer):
    assert word_placer._is_word_in_bounds("test", (7, 7), enum.Direction.HORIZONTAL)
    assert word_placer._is_word_in_bounds("test", (7, 7), enum.Direction.VERTICAL)
    assert not word_placer._is_word_in_bounds(
        "test", (7, 12), enum.Direction.HORIZONTAL
    )
    assert not word_placer._is_word_in_bounds("test", (12, 7), enum.Direction.VERTICAL)
    assert not word_placer._is_word_in_bounds(
        "verylongwordthatdoesntfit", (7, 7), enum.Direction.HORIZONTAL
    )


def test_is_grid_empty(word_placer):
    assert word_placer._is_grid_empty()
    word_placer.grid[7, 7] = "A"
    assert not word_placer._is_grid_empty()


def test_check_first_word_placement(word_placer):
    assert word_placer._check_first_word_placement(
        "test", (7, 7), enum.Direction.HORIZONTAL
    )["state"]
    assert word_placer._check_first_word_placement(
        "test", (7, 7), enum.Direction.VERTICAL
    )["state"]
    assert not word_placer._check_first_word_placement(
        "test", (0, 0), enum.Direction.HORIZONTAL
    )["state"]
    assert not word_placer._check_first_word_placement(
        "test", (14, 14), enum.Direction.VERTICAL
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
    assert word_placer._check_perpendicular_word((8, 7), "a", enum.Direction.VERTICAL)[
        "state"
    ]
    assert word_placer._check_perpendicular_word((6, 8), "x", enum.Direction.VERTICAL)[
        "state"
    ]
    assert word_placer._check_perpendicular_word((7, 10), "t", enum.Direction.VERTICAL)[
        "state"
    ]
    assert not word_placer._check_perpendicular_word(
        (7, 10), "x", enum.Direction.VERTICAL
    )["state"]


def test_check_word_placement(word_placer):
    word_placer.grid[7, 7:11] = list("tout")
    assert word_placer._check_word_placement("atout", (6, 7), enum.Direction.VERTICAL)[
        "state"
    ]
    assert word_placer._check_word_placement(
        "atoute", (7, 6), enum.Direction.HORIZONTAL
    )["state"]
    assert not word_placer._check_word_placement(
        "axout", (6, 7), enum.Direction.VERTICAL
    )["state"]


def test_is_word_placable(word_placer):
    # First word placement
    assert word_placer.is_word_placable("test", (7, 7), enum.Direction.HORIZONTAL)[
        "state"
    ]

    # Update grid
    word_placer.grid[7, 7:11] = list("test")
    # Valid placements
    assert word_placer.is_word_placable("tout", (7, 7), enum.Direction.VERTICAL)[
        "state"
    ]
    assert word_placer.is_word_placable("tester", (7, 7), enum.Direction.HORIZONTAL)[
        "state"
    ]

    # Invalid placements
    assert (
        not word_placer.is_word_placable("test", (7, 7), enum.Direction.HORIZONTAL)[
            "letter_already_placed"
        ]
        != []
    )  # Overlapping
    assert not word_placer.is_word_placable("test", (0, 0), enum.Direction.HORIZONTAL)[
        "state"
    ]  # Not touching
    assert not word_placer.is_word_placable("invalid", (6, 8), enum.Direction.VERTICAL)[
        "state"
    ]  # Invalid word


def test_is_word_placable_edge_cases(word_placer):
    # Word too long
    assert not word_placer.is_word_placable(
        "a" * 16, (7, 7), enum.Direction.HORIZONTAL
    )["state"]

    # Word at edge of grid
    assert word_placer.is_word_placable("test", (14, 7), enum.Direction.HORIZONTAL)[
        "state"
    ]
    assert not word_placer.is_word_placable("test", (14, 7), enum.Direction.VERTICAL)[
        "state"
    ]

    # Word creating invalid perpendicular word
    word_placer.grid[7, 7:11] = list("test")
    assert not word_placer.is_word_placable("ax", (6, 8), enum.Direction.VERTICAL)[
        "state"
    ]


if __name__ == "__main__":
    pytest.main()
