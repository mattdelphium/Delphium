# main.py
from config.settings import (
    MAX_GAMES_TO_SUMMARIZE,
    SUMMARY_CACHE_DIR,
    START_YEAR,
    END_YEAR,
    INCLUDE_MONTHS,
    CHESS_USERNAME
)
from fetch.chesscom import fetch_games_from_chesscom
from analyser.stockfish import analyze_single_game
from analyser.summariser import (
    summarize_single_game_with_openai,
    summarize_all_games_with_openai,
)
from utils.cache import (
    load_cached_summary,
    save_cached_summary,
    load_cached_game,
    save_cached_game,
)
import os

all_game_data = []
structured_summaries = []

def analyze_all_games():
    fetched_games = fetch_games_from_chesscom(
        CHESS_USERNAME,
        START_YEAR,
        END_YEAR,
        INCLUDE_MONTHS,
        lambda game_data, url: analyze_single_game(game_data, url, CHESS_USERNAME)
    )

    for game in fetched_games:
        all_game_data.append(game)

    if not all_game_data:
        print("❌ No games analyzed.")
        return

    for i, game in enumerate(all_game_data[:MAX_GAMES_TO_SUMMARIZE], start=1):
        print(f"🤖 Summarizing game {i} of {min(len(all_game_data), MAX_GAMES_TO_SUMMARIZE)}...")
        game_hash = game.get("hash")
        summary = load_cached_summary(CHESS_USERNAME, game_hash)
        if summary:
            print(f"✅ Found cached summary for {game_hash}")
        else:
            summary = summarize_single_game_with_openai(game)
            if summary:
                save_cached_summary(CHESS_USERNAME, game_hash, summary)

        if summary:
            structured_summaries.append(summary)

    print("\n🧠 Global Summary from GPT-4o:")
    print(summarize_all_games_with_openai(structured_summaries))

if __name__ == "__main__":
    analyze_all_games()
