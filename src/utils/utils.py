import time
from typing import TypedDict, Dict, List

from src.utils.logger_config import logger


class LetterValue(TypedDict):
    number: int
    value: int


def measure_execution_time(func):
    """
    Decorator to measure the execution time of a function
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Function {func.__name__} took {execution_time:.8f} seconds to execute")
        return result

    return wrapper


def load_letter_values(file: str) -> dict[str, LetterValue]:
    """
    Load the letter values from a file
    :param file:
    :return:
    """
    letter_values: dict[str, LetterValue] = {}
    with open(file, "r") as f:
        for line in f:
            letter, number, value = line.strip().split(" ")
            letter_values[letter.lower()] = {"number": int(number), "value": int(value)}
    return letter_values


def count_letters(letters: List) -> Dict[str, int]:
    """
    Count the number of occurrences of each letter in the list
    :param letters:
    :return:
    """
    letter_count: Dict[str, int] = {}
    for letter in letters:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1
    return letter_count


@measure_execution_time
def load_word(file: str, max_size: float = float("inf")) -> list:
    """
    Load words from a file and filter them by size
    :param file:
    :param max_size:
    :return:
    """
    result = []
    with open(file, "r") as f:
        for word in f:
            if len(word.strip()) <= max_size:
                result.append(word.strip())
    return result
