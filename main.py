from config.settings import (
    MAX_GAMES_TO_SUMMARIZE,
    SUMMARY_CACHE_DIR,
    START_YEAR,
    END_YEAR,
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
)
import os


all_game_data = []
structured_summaries = []

def analyze_all_games():
    # ✅ Pass all arguments explicitly
    fetched_games = fetch_games_from_chesscom(
        CHESS_USERNAME,
        START_YEAR,
        END_YEAR,
        analyze_single_game
    )

    for game in fetched_games:
        all_game_data.append(game)

    if not all_game_data:
        print("❌ No games analyzed.")
        return

    for i, game in enumerate(all_game_data[:MAX_GAMES_TO_SUMMARIZE], start=1):
        print(f"🤖 Summarizing game {i} of {min(len(all_game_data), MAX_GAMES_TO_SUMMARIZE)}...")
        game_hash = game.get("hash")
        cache_path = os.path.join(SUMMARY_CACHE_DIR, f"{game_hash}.json")

        if os.path.exists(cache_path):
            print(f"✅ Found cached summary: {cache_path}")
            summary = load_cached_summary(game_hash)
        else:
            summary = summarize_single_game_with_openai(game)
            if summary:
                save_cached_summary(game_hash, summary)

        if summary:
            structured_summaries.append(summary)

    print("\n🧠 Global Summary from GPT-4o:")
    print(summarize_all_games_with_openai(structured_summaries))


if __name__ == "__main__":
    analyze_all_games()
