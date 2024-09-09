from abc import ABC, abstractmethod
from typing import TypedDict, Callable

from src.game import Game


class PlaceWord(TypedDict):
    word: str
    position: tuple
    direction: str


class Player(ABC):
    def __init__(self):
        self.rack = []
        self.score = 0

    @abstractmethod
    def play(self, game: Game) -> PlaceWord:
        pass


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def play(self, game: Game) -> PlaceWord:
        # TODO: Implement this method
        pass


class ComputerPlayer(Player):
    def __init__(self, research_method: Callable[[Game], PlaceWord] = None):
        super().__init__()
        self.research_method: Callable[[Game], PlaceWord] = research_method

    def play(self, game: Game) -> PlaceWord:
        return self.research_method(game)
