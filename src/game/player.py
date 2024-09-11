from abc import ABC, abstractmethod
from typing import List

from src.utils.grid import WordPlacerChecker
from src.search_strategy.WordSearchStrategy import WordSearchStrategy
from src.utils.typing_utils import PlaceWord, Direction


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

    @abstractmethod
    def serialize(self) -> dict:
        return {
            "player_id": self.player_id,
            "rack": self.rack,
            "score": self.score_history,
        }

    @abstractmethod
    def get_valid_move(self, word_placer_checker: WordPlacerChecker) -> PlaceWord:
        """
        Get the move from the player
        :param word_placer_checker:
        :return: return a valid move, cannot return invalid moves
        """
        pass

    def display_rack(self):
        return f"rack: {', '.join(self.rack)}"

    def update_score(self, score: int):
        self.score_history.append(score)


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"Human Player {super().__repr__()}"

    def __str__(self):
        return f"Human player {super().__str__()}"

    def serialize(self) -> dict:
        return super().serialize() | {"type": "HumanPlayer"}

    @staticmethod
    def _get_coordinates() -> tuple[int, int]:
        while True:
            try:
                row = int(input("Enter the row number: "))
                col = int(input("Enter the column number: "))
                if row < 0 or col < 0:
                    print("Invalid input, please enter a positive number")
                    continue
                elif row >= 15 or col >= 15:
                    print("Invalid input, please enter a number less than 15")
                    continue
                return row, col
            except ValueError:
                print("Invalid input, please enter a number")
                continue

    @staticmethod
    def _get_direction() -> Direction:
        while True:
            fetched_direction = input("Enter the direction (across or down): ")
            match fetched_direction.lower():
                case "across":
                    return Direction.HORIZONTAL
                case "down":
                    return Direction.VERTICAL
                case _:
                    print("Invalid direction, please enter 'across' or 'down'")
                    continue

    def _check_word_validity(
        self,
        word: str,
        start_position: tuple[int, int],
        direction: Direction,
        word_placer_checker: WordPlacerChecker,
    ) -> bool:
        result = word_placer_checker.is_word_placable(word, start_position, direction)
        if not result["state"]:
            print(result["message"])
            return False
        is_letter_in_rack = all([letter in self.rack for letter in result["letter_already_placed"]])
        if not is_letter_in_rack:
            print("You do not have the required letters in your rack")
            return False
        for letter in result["letter_already_placed"]:
            self.rack.remove(letter)
        return True

    def get_valid_move(self, word_placer_checker: WordPlacerChecker) -> PlaceWord:
        print(word_placer_checker.grid)
        print(self.display_rack())
        while True:
            start_position = self._get_coordinates()
            direction = self._get_direction()
            word = input("Enter the word to place: ")
            if self._check_word_validity(
                word, start_position, direction, word_placer_checker
            ):
                break
        return PlaceWord(word=word, start_position=start_position, direction=direction)


class ComputerPlayer(Player):
    def __init__(self, word_search_strategy: WordSearchStrategy):
        super().__init__()
        self.research_method: WordSearchStrategy = word_search_strategy

    def __repr__(self):
        return f"Computer Player {super().__repr__()}"

    def __str__(self):
        return f"Computer player {super().__str__()}"

    def serialize(self) -> dict:
        return super().serialize() | {"type": "ComputerPlayer"}

    def get_valid_move(self, word_placer_checker: WordPlacerChecker) -> PlaceWord:
        return self.research_method.find_best_word(self.rack, word_placer_checker)
