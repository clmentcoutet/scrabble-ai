import enum
from typing import TypedDict, List, Dict, Optional


class Direction(enum.Enum):
    HORIZONTAL = "H"
    VERTICAL = "V"


class PlaceWord(TypedDict):
    word: str
    start_position: tuple
    direction: Direction


DEFAULT_PLACE_WORD = PlaceWord(
    word="", start_position=(0, 0), direction=Direction.HORIZONTAL
)


class ValidWord(TypedDict):
    play: PlaceWord
    letter_used: List[str]
    score: Optional[int]


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


class Result(TypedDict):
    state: bool
    letter_already_placed: List[str]
    message: str
    perpendicular_words: Dict[str, str]
