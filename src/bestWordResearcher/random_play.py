from src.game import Game
from src.player import PlaceWord


def random_play(game: Game) -> PlaceWord:
    return {"word": "test", "position": (7, 7), "direction": "HORIZONTAL"}
