# ♟️ Delphium – Chess Game Analyzer

**Delphium** is a local tool for analyzing your Chess.com games using **Stockfish** and **GPT-4o**, producing structured insights to help you improve.

---

## 🚀 Features

- ⬇️ Fetches games directly from Chess.com
- 🧠 Uses **Stockfish** for move-by-move evaluation
- 🤖 Summarizes mistakes and patterns using GPT-4o
- 💾 Caches results for speed and repeat runs
- 📊 Provides per-game insights and cross-game summaries

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/delphium.git
cd delphium
```

### 2. Set up virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your API key and username

Create a `.env` file with the following content:

```env
# .env
OPENAI_API_KEY=your-openai-api-key
CHESS_USERNAME=your-chesscom-username
```

✅ **Tip:** For sharing, use the `.env.example` file shown below.

---

## ⚙️ Example .env file

```env
# .env.example

# Your OpenAI API key (https://platform.openai.com)
OPENAI_API_KEY=sk-REPLACE_ME

# Your Chess.com username (lowercase)
CHESS_USERNAME=your-chesscom-username
```

---

## 🔧 Setup Stockfish

1. Download the [latest Stockfish binary](https://stockfishchess.org/download/).
2. Place it inside a folder named `stockfish`:

```
stockfish/stockfish
```

3. Make sure it is executable:

```bash
chmod +x stockfish/stockfish
```

---

## 🧠 Customize Prompts

Prompts are stored in the `prompts/` folder:

- `single_game_prompt.txt`: for per-game summaries
- `global_summary_prompt.txt`: for global trends across games

These use `{{GAME_JSON}}` or `{{STRUCTURED_SUMMARIES}}` placeholders, automatically filled in during runtime.

---

## ▶️ Run the Tool

```bash
python main.py
```

Delphium will:
- Fetch your games from Chess.com for the configured year range
- Analyze moves with Stockfish
- Summarize results with GPT-4o
- Output a global report at the end

---

## 📄 .gitignore

Make sure your `.gitignore` includes:

```gitignore
# Secrets and system files
.env
__pycache__/
*.pkl
cache/
stockfish/stockfish
```

---

## 🧪 Example Output

```bash
📥 Fetching games from Chess.com API...
📝 Analyzed + cached game: 47a3d...
🤖 Summarizing game 1 of 10...
✅ Found cached summary: cache/summaries/47a3d....json

🧠 Global Summary from GPT-4o:
- ♜ Common blunders: hanging pieces in early middlegame
- 📖 Strategic themes: weak d5 square, premature pawn pushes
- 🎯 Recommendations: study endgames & positional sacrifices
```

---

## 📝 License

MIT License – free to use, modify, and improve.

---

## ❤️ Contributing

If you’d like to contribute improvements (prompt tweaks, visualizations, or UI), feel free to open a pull request or suggestion.
