from src import settings
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

    def search(self, node: TreeNode, letters_count: dict, path: list, results: list):
        """
        Search for all valid words that can be formed with the given letters
        :param node:
        :param letters_count:
        :param path:
        :param results:
        :return: None but modifies the results list in place
        """
        if node.is_end_of_word:
            results.append("".join(path))

        for letter in letters_count:
            if letters_count[letter] > 0 and letter in node.children:
                letters_count[letter] -= 1
                path.append(letter)
                self.search(node.children[letter], letters_count, path, results)
                path.pop()
                letters_count[letter] += 1
            # add "*" to search for any letter
            if letter == "*" and letters_count[letter] > 0:
                letters_count[letter] -= 1
                for child in node.children:
                    path.append(child)
                    self.search(node.children[child], letters_count, path, results)
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
