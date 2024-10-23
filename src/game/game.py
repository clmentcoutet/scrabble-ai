import random
from typing import List, TypedDict, Dict

from src.game.bag import Bag, BASE_BAG
from src.utils.grid import Grid, WordPlacerChecker, compute_score
from src.game.player import Player
from src.utils.tree import Tree, BASE_TREE
from src.utils.typing_utils import PlayerMove


class GameState(TypedDict):
    """
    A game state is a dictionary containing the grid, the bag and the plays
    the integer key is the hash of the player
    """

    grid: Grid
    bag: Bag
    plays: Dict[int, PlayerMove]


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
        grid: Grid = Grid(),
        tree: Tree = BASE_TREE,
        bag: Bag = BASE_BAG,
        rack_size: int = 7,
    ):
        if len(players) < 2:
            raise ValueError("At least two players are required to play the game")
        self.players: List[Player] = players
        self.grid: Grid = grid
        self.starter_grid: Grid = grid
        self.tree: Tree = tree
        self.bag: Bag = bag
        self.starter_bag: Bag = bag
        self.rack_size: int = rack_size

        self.current_player: int = self.players[0].player_id
        self.turn: int = 0
        self.game_history: dict[int, GameState] = {}
        self.word_placer_checker = WordPlacerChecker(self.grid, self.tree)

    @property
    def score(self) -> int:
        if any([len(player.score_history) == 0 for player in self.players]):
            return 0
        return sum([player.score_history[-1] for player in self.players])

    def _list_players_str(self) -> str:
        return ", ".join([str(player) for player in self.players])

    def __str__(self):
        return f"Game with \n players: {self._list_players_str()} \n grid: {self.grid} \n tree: {self.tree} \n bag: {self.bag}"

    def serialize(self) -> dict:
        return {
            "players": [player.serialize() for player in self.players],
            "current_grid": self.grid.serialize(),
            "starter_grid": self.starter_grid.serialize(),
            "tree": self.tree.origin_file_path,
            "current_bag": self.bag.serialize(),
            "starter_bag": self.starter_bag.serialize(),
            "rack_size": self.rack_size,
            "game_history": self.game_history,
        }

    def _next_turn(self, plays: Dict[int, PlayerMove]) -> None:
        """
        Go to the next turn, a turn is when each player has played once
        - update the game history for the turn
        - update the turn number
        """

        self.game_history[self.turn] = {
            "grid": self.grid,
            "bag": self.bag,
            "plays": plays,
        }
        self.turn += 1

    def _get_current_player_index(self) -> int:
        return next(
            index
            for index, player in enumerate(self.players)
            if player.player_id == self.current_player
        )

    def _fill_rack(self, player: Player):
        nb_letters = self.rack_size - len(player.rack)
        player.rack.extend(self.bag.pick_n_random_letters(nb_letters))

    def _play_turn(self):
        plays = {}
        print(f"Turn {self.turn}")
        print(f"Players: {self._list_players_str()}")
        for player in self.players:
            print(f"Player {player.player_id} is playing")
            self.current_player = player.player_id
            self._fill_rack(player)
            print(self.grid)
            print(player.display_rack())
            play = player.get_valid_move(self.word_placer_checker)
            self.grid.place_word(**play)
            print(
                f"Player {player.player_id} played {play} and scored {player.score_history[-1]} points, new score: {sum(player.score_history)}"
            )

            plays[player.player_id] = PlayerMove(rack_before=player.rack, play=play)
            print("\n")
        self._next_turn(plays)

    def play_game(self):
        print(f"Starting game with players: {self._list_players_str()}")
        while self.bag and all([len(player.rack) > 0 for player in self.players]):
            self._play_turn()
        print(f"Game over, final score: {self.score}")
        return self.score

    def init_game(self):
        random.shuffle(self.players)
        for player in self.players:
            nb_letters = self.rack_size - len(player.rack)
            player.rack = list(self.bag.pick_n_random_letters(nb_letters))
