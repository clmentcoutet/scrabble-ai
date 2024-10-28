import concurrent.futures
import multiprocessing
from threading import Thread
from typing import List
from tqdm import tqdm
import threading

from src.game.game import Game
from src.game.player import ComputerPlayer
from src.search_strategy.UltraNaiveSearch import UltraNaiveSearch
from src.utils.logger_config import print_logger
from src.utils.typing import typed_dict as td

from typing import Dict, Tuple
from collections import defaultdict


def calculate_scores(game_history: td.GameHistory) -> Tuple[int, Dict[int, int]]:
    """
    Calculate scores for a completed game.

    Args:
        game_history: Dictionary containing player moves and scores

    Returns:
        Tuple containing total game score and player scores
    """
    player_scores = {}
    total_score = 0
    for player_id, scores in game_history["players_score"].items():
        player_score = sum(scores)
        player_scores[player_id] = player_score
        total_score += player_score

    return total_score, player_scores


# Helper function to format and print scores
def print_game_scores(game_history: td.GameHistory) -> None:
    """
    Print formatted scores for a game.

    Args:
        game_history: List of dictionaries containing player moves and scores
    """
    player_scores = game_history["players_score"]
    total_score = 0

    print("\nGame Score Summary:")
    print("-" * 20)
    for player_id, score in sorted(player_scores.items()):
        player_score = sum(score)
        print(f"Player {player_id}: {player_score} points")
        total_score += player_score
    print("-" * 20)
    print(f"Total Score: {total_score} points")


def analyze_multiple_games(game_histories: List[td.GameHistory]) -> None:
    """
    Analyze scores for multiple games and print summary statistics.

    Args:
        game_histories: List of GameHistory objects, one for each completed game
    """
    # Track statistics
    game_totals = []
    player_aggregates = defaultdict(list)

    print("\nAnalyzing Multiple Games:")
    print("=" * 40)

    # Process each game
    for game_num, history in enumerate(game_histories, 1):
        # Get scores using existing helper function
        total_score, player_scores = calculate_scores(history)
        game_totals.append(total_score)

        # Print individual game results
        print(f"\nGame {game_num}:")
        print("-" * 20)
        for player_id, score in sorted(history["players_score"].items()):
            player_score = sum(score)
            print(f"Player {player_id}: {player_score} points")
            player_aggregates[player_id].append(player_score)
        print(f"Total: {total_score} points")

    # Print overall statistics
    print("\nOverall Statistics:")
    print("=" * 40)
    print(f"Total Games Played: {len(game_histories)}")
    print(f"Average Game Total: {sum(game_totals) / len(game_totals):.1f} points")
    print(f"Highest Game Total: {max(game_totals)} points")
    print(f"Lowest Game Total: {min(game_totals)} points")


def play_computer_vs_computer_game() -> td.GameHistory:
    player_1 = ComputerPlayer(UltraNaiveSearch())
    player_2 = ComputerPlayer(UltraNaiveSearch())
    game_instance = Game([player_1, player_2])
    game_instance.init_game()
    result = game_instance.play_game()
    return result


def play_computer_vs_computer_game_thread(game_nb: int) -> td.GameHistory:
    print_logger.info(f"Starting game {game_nb} in thread {multiprocessing.current_process().pid}")
    return play_computer_vs_computer_game()

def run_multiple_games(num_games: int) -> List[td.GameHistory]:
    with multiprocessing.Pool() as pool:
        # Run the games in parallel using multiprocessing, with a progress bar
        results = list(
            tqdm(
                pool.imap_unordered(play_computer_vs_computer_game_thread, range(num_games)),
                total=num_games,
                desc="Running games",
            )
        )

    return results
