import json
import os
from openai import OpenAI

PROMPT_SINGLE_PATH = os.path.join("prompts", "game_summary_prompt.txt")
PROMPT_GLOBAL_PATH = os.path.join("prompts", "global_summary_prompt.txt")
client = OpenAI()

def load_prompt_template(path):
    with open(path, "r") as f:
        return f.read()

def summarize_single_game_with_openai(game):
    template = load_prompt_template(PROMPT_SINGLE_PATH)
    prompt = template.format(game_json=json.dumps(game, indent=2))

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        return json.loads(content[json_start:json_end])
    except Exception as e:
        print(f"❌ OpenAI error (single game): {e}")
        return None

def summarize_all_games_with_openai(structured_summaries):
    template = load_prompt_template(PROMPT_GLOBAL_PATH)
    prompt = template.format(structured_json=json.dumps(structured_summaries, indent=2))

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI error (summary): {e}")
        return None
