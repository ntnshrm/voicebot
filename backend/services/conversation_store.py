import json
import os

CONV_DIR = "../data/conversations"
os.makedirs(CONV_DIR, exist_ok=True)

MAX_TURNS = 6  # 6 user+assistant messages = 3 rounds


def load_conversation(report_id: str):
    path = f"{CONV_DIR}/{report_id}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_conversation(report_id: str, messages: list):
    # keep only last N messages
    trimmed = messages[-MAX_TURNS:]
    path = f"{CONV_DIR}/{report_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(trimmed, f, indent=2)
