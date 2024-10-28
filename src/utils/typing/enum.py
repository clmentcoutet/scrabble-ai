import enum


class Direction(enum.Enum):
    HORIZONTAL = "H"
    VERTICAL = "V"


class CellValue(enum.Enum):
    EMPTY = 0
    DOUBLE_WORD = 1
    TRIPLE_WORD = 4
    DOUBLE_LETTER = 3
    TRIPLE_LETTER = 2
    START = 5

    def __repr__(self):
        return self.value
