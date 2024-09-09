from typing import List

from src.bag import Bag
from src.grid import Grid, WordPlacer
from src.player import Player
from src.tree import Tree


class Game:
    def __init__(self, players: List[Player], grid: Grid, tree: Tree, bag: Bag):
        self.players = players
        self.grid = grid
        self.tree = tree
        self.bag = bag
        self.word_placer = WordPlacer(self.grid, self.tree)
        self.current_player = 0
