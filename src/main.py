import numpy as np

from src.grid import Direction, is_word_placable, SCORE_GRID
from src.tree import Tree
from src.utils import count_letters, measure_execution_time


def convert_to_tree(words: list) -> Tree:
    """
    Convert a list of words to a tree
    :param words: list of words
    :return: tree containing all words
    """
    tree = Tree()
    for word in words:
        tree.insert(word.lower())
    return tree


@measure_execution_time
def find_words(letters: list, tree: Tree):
    """
    Find all valid words that can be formed with the given letters
    :param letters: list of letters
    :param tree: tree containing all valid words
    :return: list of valid words
    """
    letters_count = count_letters(letters)
    results = []
    tree.search(tree.root, letters_count, [], results)
    return sorted(results, key=len, reverse=True)


def find_possible_start_positions(
    word: str,
    current_grid: np.matrix,
) -> list[tuple[int, int, Direction]]:
    """
    Find all possible start positions for a word on the current grid
    :param word:
    :param current_grid:
    :return:
    """
    result = []
    for i in range(current_grid.shape[0]):
        for j in range(current_grid.shape[1]):
            for direction in Direction:
                if is_word_placable((i, j), word, direction, current_grid):
                    result.append((i, j, direction))


def find_best_placement(
    word: str,
    letters_values: dict,
    current_grid: np.matrix,
    score_grid: np.matrix = SCORE_GRID,
) -> tuple[int, int, Direction]:
    """
    Find the best placement for a word on the current grid
    :param word:
    :param letters_values:
    :param current_grid:
    :param score_grid:
    :return:
    """
    pass
