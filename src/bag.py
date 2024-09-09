import random


class Bag:
    def __init__(self, letter_distribution: dict[str, int]):
        self.letter_distribution: dict[str, int] = letter_distribution
        self.bag: list = self._create_bag()

    def __len__(self) -> int:
        return len(self.bag)

    def __str__(self) -> str:
        return str(self.bag)

    def _create_bag(self) -> list[str]:
        bag = []
        for letter, count in self.letter_distribution.items():
            bag.extend([letter] * count)
        return bag

    def is_in_bag(self, letter: str) -> bool:
        return letter in self.bag

    def pick_random_letter(self) -> str:
        return self.bag.pop(random.randint(0, len(self.bag) - 1))
