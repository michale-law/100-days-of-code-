# game.py
import random
import json
import os
from typing import List, Dict, Optional


class GameBrain:
    """Game engine for flashcard pairs.

    Accepts either:
      - a list of pairs: [{"en":"...","es":"..."}, ...]
      - a dict mapping deck_name -> list of pairs: {"spanish_basic": [...], ...}

    If a dict is provided and no deck_name argument is given, the first key
    will be used (useful for files that contain a single named deck).
    """

    def __init__(self, deck, deck_name: Optional[str] = None):
        # Normalize deck input into (self.deck_name, self.deck:list)
        if isinstance(deck, dict):
            if deck_name:
                self.deck_name = deck_name
                self.deck: List[Dict[str, str]] = list(deck.get(deck_name, []))
            else:
                keys = list(deck.keys())
                if keys:
                    self.deck_name = keys[0]
                    self.deck = list(deck[self.deck_name])
                else:
                    self.deck_name = deck_name or "unknown"
                    self.deck = []
        else:
            # deck is a list
            self.deck = list(deck) if deck else []
            self.deck_name = deck_name or "unknown"

        self.score = 0

    def pick_pair(self) -> Optional[Dict[str, str]]:
        """Pick a random remaining pair (None if empty)."""
        return random.choice(self.deck) if self.deck else None

    def check_answer(self, user_input: str, current_pair: Dict[str, str]) -> bool:
        """Compare user input to English translation; remove on correct."""
        is_correct = user_input.strip().lower() == current_pair.get("en", "").strip().lower()
        if is_correct:
            self.score += 1
            if current_pair in self.deck:
                self.deck.remove(current_pair)
            print("✅ Correct!")
        else:
            print(f"❌ Wrong! Correct: '{current_pair.get('en', '')}'")
        return is_correct

    def save_game(self, save_name: str, save_dir: str = "saves") -> str:
        """Save deck name, remaining cards, and score to JSON. Returns path."""
        os.makedirs(save_dir, exist_ok=True)
        payload = {
            "deck_name": self.deck_name,
            "remaining": self.deck,
            "score": self.score,
        }
        path = os.path.join(save_dir, f"{save_name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return path


# Optional console helpers (not used by GUI, but kept if you want CLI play)
def load_saved_deck(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "remaining" in data and "deck_name" in data:
        return {data["deck_name"]: data["remaining"]}
    return data
