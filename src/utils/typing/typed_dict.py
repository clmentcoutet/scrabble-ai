from typing import TypedDict, List, Dict

from src.utils.typing.enum import Direction


class PlaceWord(TypedDict):
    word: str
    start_position: tuple
    direction: Direction


class ValidWord(TypedDict):
    play: PlaceWord
    letter_used: List[str]
    score: int


class PlayerMove(TypedDict):
    rack_before: List[str]
    valid_word: ValidWord


class Result(TypedDict):
    state: bool
    letter_already_placed: List[str]
    message: str
    perpendicular_words: List[PlaceWord]


class GameHistory(TypedDict):
    history: List[Dict[int, PlayerMove]]
    players_score: Dict[int, List[int]]
