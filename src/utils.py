# utils.py — Helpers for chat storage, sentiment, and canned replies

import json
from pathlib import Path
from textblob import TextBlob
from typing import List, Dict
from datetime import datetime

# --- Data directory setup ---
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
CHAT_FILE = DATA_DIR / "chats.json"

def load_chats() -> Dict:
    """Load previous chat sessions from JSON."""
    if CHAT_FILE.exists():
        return json.loads(CHAT_FILE.read_text(encoding="utf-8"))
    return {"sessions": []}

def save_chat(session: Dict):
    """Save current chat session with timestamp."""
    data = load_chats()
    session["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["sessions"].append(session)
    CHAT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def sentiment_score(text: str) -> float:
    """Return sentiment polarity between -1 (negative) and 1 (positive)."""
    t = TextBlob(text)
    return round(t.sentiment.polarity, 2)

# --- Canned Responses (Quick Replies) ---
CANNED = [
    "Hello! How can I assist you today?",
    "I'm sorry to hear that — can you share the order/issue ID?",
    "Thanks, I’ll escalate this to our technical team. Expect an update soon!",
    "Please try restarting the app and let me know the exact error message.",
    "Sure! Could you clarify the problem a bit more?",
    "Your feedback is valuable — I’ll make sure it’s forwarded to the right team."
]