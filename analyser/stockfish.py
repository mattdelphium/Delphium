# analyser/stockfish.py
import io
import hashlib
import chess
import chess.pgn
import chess.engine
from config.settings import STOCKFISH_PATH, ENGINE_DEPTH, EVAL_THRESHOLDS
from utils.cache import load_cached_game, save_cached_game

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

def analyze_single_game(game_data, archive_url, username):
    game_obj = chess.pgn.read_game(io.StringIO(game_data))
    if not game_obj:
        return None

    game_hash = get_game_hash(game_data)
    cached = load_cached_game(username, game_hash)
    if cached:
        print(f"✅ Loaded cached game: {game_hash}")
        return cached

    white = game_obj.headers.get("White", "Unknown")
    black = game_obj.headers.get("Black", "Unknown")

    if username.lower() == white.lower():
        player_color = "White"
        player_to_coach = white
    elif username.lower() == black.lower():
        player_color = "Black"
        player_to_coach = black
    else:
        player_color = "Unknown"
        player_to_coach = username

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
        "moves": move_data,
        "white": white,
        "black": black,
        "result": game_obj.headers.get("Result", "*"),
        "player_color": player_color,
        "player_to_coach": player_to_coach,
    }
    save_cached_game(username, game_hash, result)
    print(f"📝 Analyzed + cached game: {game_hash}")
    return result