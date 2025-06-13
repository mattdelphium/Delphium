import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
STOCKFISH_PATH = "./stockfish/stockfish"
ENGINE_DEPTH = 15
EVAL_THRESHOLDS = {"blunder": 300, "mistake": 100, "inaccuracy": 50}
START_YEAR = 2025
END_YEAR = 2025
INCLUDE_MONTHS = [5, 6]
CACHE_DIR = "./cache"
SUMMARY_CACHE_DIR = os.path.join(CACHE_DIR, "summaries")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(SUMMARY_CACHE_DIR, exist_ok=True)

MAX_GAMES_TO_SUMMARIZE = 20

# client = OpenAI()
CHESS_USERNAME = os.getenv("CHESS_USERNAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")