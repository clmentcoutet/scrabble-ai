from abc import ABC, abstractmethod
from typing import List, Tuple
from collections import Counter

from src.engine.grid import compute_total_word_score
from src.engine.word_checker import WordPlacerChecker
from src.search_strategy.WordSearchStrategy import WordSearchStrategy
from src.utils.logger_config import logger, print_logger
from src.utils.typing import enum, typed_dict as td


class Player(ABC):
    """
    Abstract class for a player in the game

    Attributes:
    - rack: List[str]: The letters that the player has
    - score: List[int]: The score of the player, updated after each move
    - nb_skip_turn: int: The number of turn the player has skipped

    Methods:
    - player_id: int: The hash of the player object
    """

    def __init__(self):
        self.rack: List[str] = []
        self.score_history: List[int] = []
        self.nb_skip_turn: int = 0

    @property
    def player_id(self) -> int:
        return hash(self)

    @abstractmethod
    def __repr__(self):
        return f"{self.player_id} with rack {self.rack} and total score {sum(self.score_history)}"

    @abstractmethod
    def __str__(self):
        return f"{self.player_id} with rack {self.rack} and total score {sum(self.score_history)}"

    @abstractmethod
    def serialize(self) -> dict:
        return {
            "player_id": self.player_id,
            "rack": self.rack,
            "score": self.score_history,
        }

    @abstractmethod
    def get_valid_move(self, word_placer_checker: WordPlacerChecker) -> td.ValidWord:
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

    def remove_from_rack(self, letter: str | List[str]):
        if isinstance(letter, str):
            self.rack.remove(letter)
        else:
            for char in letter:
                if char in self.rack:
                    self.rack.remove(char)
                elif "*" in self.rack:
                    self.rack.remove("*")


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
                    print_logger.info("Invalid input, please enter a positive number")
                    continue
                elif row >= 15 or col >= 15:
                    print_logger.info(
                        "Invalid input, please enter a number less than 15"
                    )
                    continue
                return row, col
            except ValueError:
                print_logger.info("Invalid input, please enter a number")
                continue

    @staticmethod
    def _get_direction() -> enum.Direction:
        while True:
            fetched_direction = input("Enter the direction (across or down): ")
            match fetched_direction.lower():
                case "across":
                    return enum.Direction.HORIZONTAL
                case "down":
                    return enum.Direction.VERTICAL
                case _:
                    print_logger.info(
                        "Invalid direction, please enter 'across' or 'down'"
                    )
                    continue

    def _check_word_validity(
        self,
        word: str,
        start_position: tuple[int, int],
        direction: enum.Direction,
        word_placer_checker: WordPlacerChecker,
    ) -> Tuple[bool, td.ValidWord | None]:
        result = word_placer_checker.is_word_placable(word, start_position, direction)
        logger.debug(result)
        if not result["state"]:
            print_logger.info(result["message"])
            return False, None
        is_letter_in_rack = all(
            [letter in self.rack + result["letter_already_placed"] for letter in word]
        )
        if not is_letter_in_rack:
            print_logger.info("You do not have the required letters in your rack")
            return False, None
        # Remove the letters from the rack
        place_word = word_placer_checker.get_full_word(word, start_position, direction)
        # Update the score
        computed_score = compute_total_word_score(
            place_word,
            result["perpendicular_words"],
            len(result["letter_already_placed"]),
        )
        return True, td.ValidWord(
            play=place_word,
            letter_used=list(
                Counter(list(word)) - Counter(result["letter_already_placed"])
            ),
            score=computed_score,
        )

    def get_valid_move(self, word_placer_checker: WordPlacerChecker) -> td.ValidWord:
        while True:
            start_position = self._get_coordinates()
            direction = self._get_direction()
            word = input("Enter the word to place: ")
            result = self._check_word_validity(
                word, start_position, direction, word_placer_checker
            )
            if result[0]:
                return result[1]


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

    def get_valid_move(self, word_placer_checker: WordPlacerChecker) -> td.ValidWord:
        return self.research_method.find_best_word(self.rack, word_placer_checker)
