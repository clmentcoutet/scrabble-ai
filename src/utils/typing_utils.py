import enum
from typing import TypedDict, List


class PlaceWord(TypedDict):
    word: str
    position: tuple
    direction: str


class PlayerMove(TypedDict):
    rack_before: List[str]
    play: PlaceWord


class CellValue(enum.Enum):
    EMPTY = 0
    DOUBLE_WORD = 1
    TRIPLE_WORD = 4
    DOUBLE_LETTER = 3
    TRIPLE_LETTER = 2
    START = 5

    def __repr__(self):
        return self.value


class Direction(enum.Enum):
    HORIZONTAL = "H"
    VERTICAL = "V"


class Result(TypedDict):
    state: bool
    letter_already_placed: List[str]
    message: str
    has_perpendicular_word: bool