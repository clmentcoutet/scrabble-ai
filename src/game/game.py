from typing import List, TypedDict, Dict

from src.game.bag import Bag, BASE_BAG
from src.utils.grid import Grid
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

    def init_game(self):
        for player in self.players:
            for _ in range(self.rack_size):
                try:
                    player.rack.append(self.bag.pick_random_letter())
                except ValueError:
                    break
