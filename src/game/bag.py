import random

from src import settings
from src.utils.utils import LetterValue, load_letter_values


class Bag:
    def __init__(self, letter_distribution: dict[str, LetterValue]):
        self.letter_distribution: dict[str, LetterValue] = letter_distribution
        self.bag: list = self._create_bag()

    def __len__(self) -> int:
        return len(self.bag)

    def __str__(self) -> str:
        return f"Bag with {len(self.bag)} letters"

    def _create_bag(self) -> list[str]:
        bag = []
        for letter, values in self.letter_distribution.items():
            bag.extend([letter] * values["number"])
        return bag

    def serialize(self) -> dict:
        return {
            "letter_distribution": self.letter_distribution,
            "bag": self.bag,
        }

    def is_in_bag(self, letter: str) -> bool:
        return letter in self.bag

    def pick_random_letter(self) -> str:
        if not self.bag:
            raise ValueError("Bag is empty")
        return self.bag.pop(random.randint(0, len(self.bag) - 1))


BASE_BAG = Bag(load_letter_values(settings.LETTERS_VALUES_PATH))