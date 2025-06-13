import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_chesscom_archives(username):
    print("📥 Fetching games from Chess.com API...")
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
        return res.json().get("archives", [])
    except Exception as e:
        print(f"❌ Failed to fetch archive index: {e}")
        return []

def fetch_games_from_chesscom(username, start_year, end_year, months, analyze_func):
    print("📥 Fetching archives...")
    all_results = []
    archive_urls = fetch_chesscom_archives(username)

    for archive_url in archive_urls:
        year, month = map(int, archive_url.split("/")[-2:])
        if not (start_year <= year <= end_year):
            continue
        if months and month not in months:
            continue

        try:
            res = requests.get(archive_url, headers={"User-Agent": "Mozilla/5.0"})
            res.raise_for_status()
            games = res.json().get("games", [])

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for game in games:
                    if "pgn" not in game:
                        continue
                    game_data = game["pgn"]
                    # ✅ CORRECT: Pass both required arguments
                    futures.append(executor.submit(analyze_func, game_data, archive_url))

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        all_results.append(result)

        except Exception as e:
            print(f"⚠️ Failed to process {archive_url}: {e}")

    return all_results
