class TreeNode:
    """
    Node of the tree data structure
    """

    def __init__(self):
        self.children: dict = {}
        self.is_end_of_word: bool = False


class Tree:
    """
    Tree data structure to store a list of words
    """

    def __init__(self):
        self.root: TreeNode = TreeNode()

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

    def search(self,
               node: TreeNode,
               letters_count: dict,
               path: list,
               results: list):
        """
        Search for all valid words that can be formed with the given letters
        :param node:
        :param letters_count:
        :param path:
        :param results:
        :return:
        """
        if node.is_end_of_word:
            results.append(''.join(path))

        for letter in letters_count:
            if letters_count[letter] > 0 and letter in node.children:
                letters_count[letter] -= 1
                path.append(letter)
                self.search(node.children[letter], letters_count, path, results)
                path.pop()
                letters_count[letter] += 1
            # add "*" to search for any letter
            if letter == '*' and letters_count[letter] > 0:
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
        print(f"Checking word is_word {word}")
        node = self.root
        for letter in word:
            print(letter)
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_end_of_word
