from abc import ABC, abstractmethod
from typing import List

from src.utils.grid import WordPlacerChecker
from src.search_strategy.WordSearchStrategy import WordSearchStrategy
from src.utils.typing_utils import PlaceWord


class Player(ABC):
    """
    Abstract class for a player in the game

    Attributes:
    - rack: List[str]: The letters that the player has
    - score: List[int]: The score of the player, updated after each move

    Methods:
    - player_id: int: The hash of the player object
    """

    def __init__(self):
        self.rack: List[str] = []
        self.score_history: List[int] = []

    @property
    def player_id(self) -> int:
        return hash(self)

    @abstractmethod
    def __repr__(self):
        return f"{self.player_id} with rack {self.rack} and score {self.score_history}"

    @abstractmethod
    def __str__(self):
        return f"{self.player_id} with rack {self.rack} and score {self.score_history}"

    def serialize(self) -> dict:
        return {
            "player_id": self.player_id,
            "rack": self.rack,
            "score": self.score_history,
        }

    @abstractmethod
    def get_move(self, word_placer_checker: WordPlacerChecker) -> PlaceWord:
        pass


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"Human Player {super().__repr__()}"

    def __str__(self):
        return f"Human player {super().__str__()}"

    def get_move(self, word_placer_checker: WordPlacerChecker) -> PlaceWord:
        # TODO: Implement this method
        raise NotImplementedError("Method get_move not implemented")


class ComputerPlayer(Player):
    def __init__(self, word_search_strategy: WordSearchStrategy):
        super().__init__()
        self.research_method: WordSearchStrategy = word_search_strategy

    def __repr__(self):
        return f"Computer Player {super().__repr__()}"

    def __str__(self):
        return f"Computer player {super().__str__()}"

    def get_move(self, word_placer_checker: WordPlacerChecker) -> PlaceWord:
        return self.research_method.find_best_word(self.rack, word_placer_checker)
