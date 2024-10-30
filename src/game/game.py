import random
import time
from typing import List, Dict

from typing_extensions import Optional

from src.game.bag import Bag, BASE_BAG
from src.engine.grid import Grid, SCORE_GRID
from src.engine.word_checker import WordPlacerChecker
from src.game.player import Player
from src.engine.tree import Tree, BASE_TREE
from src.settings.logger_config import print_logger
from src.utils.typing import typed_dict as td


class Game:
    """
    A game is a class that represents a game of scrabble

    :param players: list of players
    :param grid: the grid at the start of the game
    :param tree: the word trie of the game
    :param bag: the bag at the start of the game
    :param rack_size: the size of the rack of the players

    Attributes:
    - players: list of players
    - grid: the grid of the game, where the letters are placed
    - starter_grid: the grid at the start of the game (immutable)
    - tree: the word trie of the game
    - bag: the bag of the game, where the letters are picked
    - starter_bag: the bag at the start of the game (immutable)
    - rack_size: the size of the rack of the players
    - current_player: the id of the current player (hash of the player object)
    - game_history: a dictionary containing the game states at each turn, indexed by turn number
        a state is registered after each turn
    """

    def __init__(
        self,
        players: List[Player],
        *,
        grid: Optional[
            Grid
        ] = None,  # Default to None, allowing us to create a unique instance per game
        tree: Tree = BASE_TREE,
        bag: Optional[Bag] = None,  # Set up the bag similarly
        score_grid: Optional[Grid] = None,
        rack_size: int = 7,
    ):
        if len(players) < 2:
            raise ValueError("At least two players are required to play the game")

        # Ensure a unique Grid instance per game
        self.players: List[Player] = players
        self.grid: Grid = grid if grid is not None else Grid()
        self.starter_grid: Grid = self.grid
        self.tree: Tree = tree
        self.bag: Bag = bag.copy() if bag is not None else BASE_BAG.copy()
        self.score_grid: Grid = score_grid if score_grid is not None else SCORE_GRID
        self.starter_bag: Bag = self.bag
        self.rack_size: int = rack_size

        self.turn: int = 0
        self.game_history: td.GameHistory = td.GameHistory(history=[], players_score={})
        self.word_placer_checker = WordPlacerChecker(self.grid, self.tree)

    @property
    def score(self) -> int:
        if any([len(player.score_history) == 0 for player in self.players]):
            return 0
        return sum([sum(player.score_history) for player in self.players])

    def _list_players_str(self) -> str:
        return ", ".join([str(player) for player in self.players])

    def __str__(self):
        return f"Game with \n players: {self._list_players_str()} \n grid: {self.grid} \n tree: {self.tree} \n bag: {self.bag}"

    def serialize(self) -> dict:
        return {
            "players": [player.serialize() for player in self.players],
            "starter_grid": self.starter_grid.serialize(),
            "starter_bag": self.starter_bag.serialize(),
            "tree": self.tree.origin_file_path,
            "rack_size": self.rack_size,
            "game_history": self.game_history,
        }

    def _next_turn(self, plays: Dict[str, td.PlayerMove]) -> None:
        """
        Go to the next turn, a turn is when each player has played once
        - update the game history for the turn
        - update the turn number
        """

        self.game_history["history"].append(plays)
        self.turn += 1

    def _fill_rack(self, player: Player):
        nb_letters = self.rack_size - len(player.rack)
        player.rack.extend(self.bag.pick_n_random_letters(nb_letters))

    def _play_turn(self):
        plays = {}
        print_logger.info(f"Turn {self.turn}")
        print_logger.info(f"Players: {self._list_players_str()}")
        for player in self.players:
            print_logger.info(f"Player {player.player_id} is playing")
            self._fill_rack(player)
            print_logger.info(self.grid)
            print_logger.info(player.display_rack())
            previous_race = player.rack.copy()
            valid_word = player.get_valid_move(
                self.word_placer_checker, self.score_grid
            )
            player.remove_from_rack(valid_word["letter_used"])
            player.update_score(valid_word["score"])
            play = valid_word["play"]
            self.grid.place_word(**play)
            # if the player played no word, skip the turn and reroll the rack
            if len(play["word"]) == 0:
                player.nb_skip_turn += 1
                # reroll the rack
                self.bag.put_back(player.rack)
                player.rack = []
                self._fill_rack(player)

            print_logger.info(
                f"Player {player.player_id} played {play} and scored {player.score_history[-1]} points, new score: {sum(player.score_history)}"
            )

            plays[player.player_id] = td.PlayerMove(
                rack_before=previous_race, valid_word=valid_word
            )
            print_logger.info("\n")
        self._next_turn(plays)

    def play_game(self) -> td.GameHistory:
        print_logger.info(f"Starting game with players: {self._list_players_str()}")
        while any([len(player.rack) > 0 for player in self.players]) and all(
            [player.nb_skip_turn < 3 for player in self.players]
        ):
            self._play_turn()
            time.sleep(0.1)
        print_logger.info(f"Game over, final score: {self.score}")
        print_logger.info(f"Players: {self._list_players_str()}")
        self.game_history["players_score"] = {
            player.player_id: player.score_history for player in self.players
        }
        return self.game_history

    def init_game(self):
        random.shuffle(self.players)
        for player in self.players:
            nb_letters = self.rack_size - len(player.rack)
            player.init_player(rack=list(self.bag.pick_n_random_letters(nb_letters)))
