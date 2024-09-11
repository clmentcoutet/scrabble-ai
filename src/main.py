import random
from typing import List

from src.game.game import Game
from src.game.player import HumanPlayer
from src.utils.tree import Tree
from src.utils.utils import count_letters, measure_execution_time


@measure_execution_time
def find_words(letters: list, tree: Tree) -> List[str]:
    """
    Find all valid words that can be formed with the given letters
    :param letters: list of letters
    :param tree: tree containing all valid words
    :return: list of valid words
    """
    letters_count = count_letters(letters)
    results: List[str] = []
    tree.search(tree.root, letters_count, [], results)
    return sorted(results, key=len, reverse=True)


if __name__ == "__main__":
    random.seed(42)
    player_1 = HumanPlayer()
    player_2 = HumanPlayer()
    game_instance = Game([player_1, player_2])
    game_instance.init_game()
    game_instance.play_game()
