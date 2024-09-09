
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
