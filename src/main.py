import random

from src.game.game import Game
from src.game.player import ComputerPlayer
from src.game_thread import analyze_multiple_games, run_multiple_games
from src.search_strategy.NaiveSearch import NaiveSearch
from src.utils.typing import typed_dict as td


def play_player_vs_computer_game() -> td.GameHistory:
    player_1 = ComputerPlayer(NaiveSearch())
    player_2 = ComputerPlayer(NaiveSearch())
    game_instance = Game([player_1, player_2])
    game_instance.init_game()
    result = game_instance.play_game()
    return result


if __name__ == "__main__":
    _a = 0
    #random.seed(42)
    analyze_multiple_games(run_multiple_games(100))
    # play_player_vs_computer_game()
