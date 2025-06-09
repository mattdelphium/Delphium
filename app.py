import os
import glob
import io
import json
import time
import chess.pgn
import chess.engine
import requests
import hashlib
import pickle
from openai import OpenAI
from datetime import datetime
from time import sleep
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

# Configuration
STOCKFISH_PATH = "./stockfish/stockfish"
ENGINE_DEPTH = 15
EVAL_THRESHOLDS = {"blunder": 300, "mistake": 100, "inaccuracy": 50}
START_YEAR = 2025
END_YEAR = 2025
CACHE_DIR = "./cache"
SUMMARY_CACHE_DIR = os.path.join(CACHE_DIR, "summaries")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(SUMMARY_CACHE_DIR, exist_ok=True)

MAX_GAMES_TO_SUMMARIZE = 10

client = OpenAI()
openai_api_key = os.getenv("OPENAI_API_KEY")
chess_username = os.getenv("CHESS_USERNAME")

all_game_data = []
structured_summaries = []

def classify_move_quality(eval_diff):
    if eval_diff is None:
        return "unknown"
    if eval_diff >= EVAL_THRESHOLDS["blunder"]:
        return "blunder"
    elif eval_diff >= EVAL_THRESHOLDS["mistake"]:
        return "mistake"
    elif eval_diff >= EVAL_THRESHOLDS["inaccuracy"]:
        return "inaccuracy"
    return "ok"

def get_game_hash(pgn_text):
    return hashlib.md5(pgn_text.encode("utf-8")).hexdigest()

def load_cached_game(game_hash):
    path = os.path.join(CACHE_DIR, f"{game_hash}.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_cached_game(game_hash, data):
    path = os.path.join(CACHE_DIR, f"{game_hash}.pkl")
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_cached_summary(game_hash):
    path = os.path.join(SUMMARY_CACHE_DIR, f"{game_hash}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_cached_summary(game_hash, summary):
    path = os.path.join(SUMMARY_CACHE_DIR, f"{game_hash}.json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)

def summarize_single_game_with_openai(game):
    prompt = f"""
You are a chess coach AI. Here's Stockfish analysis for one game. Provide a structured JSON summary like this:

{{
  "opening": "...",
  "key_mistakes": [
    {{
      "move": "...",
      "reason": "...",
      "better_move": "...",
      "type": "strategic/tactical",
      "fen": "..."
    }}
  ],
  "themes": ["..."],
  "recommendations": ["..."]
}}

In your explanations:
- Clearly describe why each move was bad using natural chess language.
- Include tactical or strategic consequences (e.g. "lost a pawn", "allowed a fork").
- Include one FEN per key mistake that captures the board just before the mistake, to help illustrate the error.

Game:
{json.dumps(game, indent=2)}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()

        # Try to extract the first valid JSON block from response
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        raw_json = content[json_start:json_end]

        return json.loads(raw_json)

    except Exception as e:
        print(f"❌ OpenAI error (single game): {e}")
        return None

def summarize_all_games_with_openai(structured_games):
    prompt = f"""
You are a world-class chess coach AI. Below are structured summaries of multiple games, including common blunders and themes.

Your job:
- Detect recurring tactical/strategic problems.
- Describe them in clear, natural chess language.
- Reference specific moves (e.g., Nd6, Qd3), but explain their **impact** (e.g., "lost central control", "allowed fork").
- If a FEN is provided, briefly describe the position and how the blunder affected it.
- DO NOT just repeat common advice like "study tactics" without giving concrete examples.
- Prioritize clarity and insight over verbosity.

Your response should include:
- ♟ Recurring patterns with detailed explanations.
- ♜ Noteworthy strategic mistakes and tactical themes.
- 🎯 Improvement suggestions with examples.
- 📖 Use coaching language: describe positions and consequences (e.g., "Nd6 allowed a bishop capture and doubled the pawns on the d-file").

Structured game summaries:
{json.dumps(structured_games, indent=2)}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI error (summary): {e}"

def analyze_single_game(game_data, archive_url):
    game_obj = chess.pgn.read_game(io.StringIO(game_data))
    if not game_obj:
        return None

    game_hash = get_game_hash(game_data)
    cached = load_cached_game(game_hash)
    if cached:
        print(f"✅ Loaded cached game: {game_hash}")
        return cached

    board = game_obj.board()
    move_data = []
    prev_eval = None

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        for i, move in enumerate(game_obj.mainline_moves(), start=1):
            san = board.san(move)
            info = engine.analyse(board, chess.engine.Limit(depth=ENGINE_DEPTH))
            pv = info.get("pv", [])
            best_move = pv[0] if pv else None
            best_move_san = board.san(best_move) if best_move else None

            current_eval = info.get("score").relative.score(mate_score=10000) if info.get("score") else None
            eval_diff = abs(current_eval - prev_eval) if prev_eval is not None and current_eval is not None else None
            quality = classify_move_quality(eval_diff) if best_move_san and san != best_move_san else "ok"

            move_info = {
                "move_number": i,
                "fen": board.fen(),
                "played_move": san,
                "best_move": best_move_san,
                "eval": current_eval,
                "eval_diff": eval_diff,
                "quality": quality
            }
            move_data.append(move_info)
            board.push(move)
            prev_eval = current_eval

    result = {
        "source": archive_url,
        "hash": game_hash,
        "moves": move_data
    }
    save_cached_game(game_hash, result)
    print(f"📝 Analyzed + cached game: {game_hash}")
    return result

def analyze_chesscom_json_games():
    print("📥 Fetching games from Chess.com API...")

    headers = {"User-Agent": "Mozilla/5.0"}
    archive_index_url = f"https://api.chess.com/pub/player/{chess_username}/games/archives"

    try:
        res = requests.get(archive_index_url, headers=headers)
        res.raise_for_status()
        archives = res.json().get("archives", [])
    except Exception as e:
        print(f"❌ Failed to fetch archive index: {e}")
        return

    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for archive_url in archives:
            try:
                year, month = map(int, archive_url.split("/")[-2:])
                if year < START_YEAR or year > END_YEAR:
                    continue

                res = requests.get(archive_url, headers=headers)
                res.raise_for_status()
                games = res.json().get("games", [])

                for game in games:
                    if "pgn" not in game:
                        continue
                    game_data = game["pgn"]
                    futures.append(executor.submit(analyze_single_game, game_data, archive_url))

            except Exception as e:
                print(f"⚠️ Failed to process {archive_url}: {e}")

        for future in as_completed(futures):
            result = future.result()
            if result:
                all_game_data.append(result)

def analyze_all_games():
    analyze_chesscom_json_games()
    if not all_game_data:
        print("❌ No games analyzed.")
        return

    for i, game in enumerate(all_game_data[:MAX_GAMES_TO_SUMMARIZE], start=1):
        print(f"🤖 Summarizing game {i} of {min(len(all_game_data), MAX_GAMES_TO_SUMMARIZE)}...")
        game_hash = game.get("hash")
        if not game_hash:
            print(f"⚠️ Warning: Game missing 'hash' key. Skipping cache lookup.")
            summary = None
        else:
            cache_path = os.path.join(SUMMARY_CACHE_DIR, f"{game_hash}.json")
            if os.path.exists(cache_path):
                print(f"✅ Found cached summary at: {cache_path}")
            else:
                print(f"🔍 No cached summary at: {cache_path}")
            summary = load_cached_summary(game_hash)
        if summary:
            print(f"✅ Loaded cached summary: {game_hash}")
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
