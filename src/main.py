import random

from src.game.game import Game
from src.game.player import HumanPlayer, ComputerPlayer
from src.search_strategy.UltraNaiveSearch import UltraNaiveSearch

def play_human_vs_human_game():
    player_1 = HumanPlayer()
    player_2 = HumanPlayer()
    game_instance = Game([player_1, player_2])
    game_instance.init_game()
    game_instance.play_game()


def play_human_vs_computer_game():
    player_1 = HumanPlayer()
    player_2 = ComputerPlayer(UltraNaiveSearch())
    game_instance = Game([player_1, player_2])
    game_instance.init_game()
    game_instance.play_game()


def play_computer_vs_computer_game():
    player_1 = ComputerPlayer(UltraNaiveSearch())
    player_2 = ComputerPlayer(UltraNaiveSearch())
    game_instance = Game([player_1, player_2])
    game_instance.init_game()
    game_instance.play_game()


if __name__ == "__main__":
    #random.seed(42)
    #play_human_vs_human_game()
    #play_human_vs_computer_game()
    play_computer_vs_computer_game()
