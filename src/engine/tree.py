from typing import Dict, List, Optional

from src.settings import settings
from src.utils.utils import load_word


class TreeNode:
    """
    Node of the tree data structure
    """

    def __init__(self) -> None:
        self.children: dict = {}
        self.is_end_of_word: bool = False


class Tree:
    """
    Tree data structure to store a list of words
    """

    def __init__(self, origin_file_path: str = settings.FRENCH_DICTIONARY_PATH):
        self.origin_file_path = origin_file_path
        self.root: TreeNode = TreeNode()

    def __str__(self):
        return f"Tree with root {self.root}"

    def insert(self, word: str):
        """
        Insert a word into the tree
        :param word:
        :return:
        """
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TreeNode()
            node = node.children[letter]
        node.is_end_of_word = True

    def search(
        self,
        node: TreeNode,
        letters_count: Dict,
        path: List,
        results: List,
        *,
        constraint: Optional[Dict[int, str]] = None,
    ):
        """
        Search for all valid words that can be formed with the given letters, respecting position constraints
        :param node: Current node in the trie
        :param letters_count: Dictionary counting available letters
        :param path: Current word being built
        :param results: List to store valid words
        :param constraint: Dictionary mapping positions to required letters, e.g., {0: 'a'} means 'a' must be at index 0
        :return: None but modifies the results list in place
        """
        current_pos = len(path)
        # Early constraint check - if current position has a constraint, only proceed if it matches
        if constraint and constraint.get(current_pos, {}):
            required_letter = constraint[current_pos]
            # If we're at a constraint position but don't have the required letter, return early
            if (
                required_letter not in node.children
                or letters_count.get(required_letter, 0) <= 0
            ):
                return
            # Process only the constrained letter
            letters_count[required_letter] -= 1
            path.append(required_letter)
            self.search(
                node.children[required_letter],
                letters_count,
                path,
                results,
                constraint=constraint,
            )
            path.pop()
            letters_count[required_letter] += 1
            return

        # If we've built a valid word and all constraints are satisfied, add it to results
        if node.is_end_of_word:
            # Check if word length satisfies all constraints
            if not constraint or all(pos < len(path) for pos in constraint.keys()):
                results.append("".join(path))

        # Process regular letters
        for letter in letters_count:
            if letters_count[letter] > 0 and letter in node.children:
                letters_count[letter] -= 1
                path.append(letter)
                self.search(
                    node.children[letter],
                    letters_count,
                    path,
                    results,
                    constraint=constraint,
                )
                path.pop()
                letters_count[letter] += 1

            # Handle wildcard "*" case
            if letter == "*" and letters_count[letter] > 0:
                letters_count[letter] -= 1
                for child in node.children:
                    # Skip if this position has a constraint and child doesn't match
                    if (
                        constraint
                        and constraint.get(current_pos, {})
                        and child != constraint[current_pos]
                    ):
                        continue

                    path.append(child)
                    self.search(
                        node.children[child],
                        letters_count,
                        path,
                        results,
                        constraint=constraint,
                    )
                    path.pop()
                letters_count[letter] += 1

    def is_word(self, word: str) -> bool:
        """
        Check if a word is in the tree
        :param word:
        :return:
        """
        node = self.root
        for letter in word:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_end_of_word


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


BASE_TREE = convert_to_tree(
    load_word(settings.FRENCH_DICTIONARY_PATH, settings.MAX_WORD_SIZE)
)
