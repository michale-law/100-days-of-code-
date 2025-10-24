# app.py
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from game import GameBrain  # <- matches game.py

# --- Root window ---
root = tk.Tk()
root.title("Flashcard Game")
title_lbl = tk.Label(root, text="Spanish Card Match", font=("Helvetica", 16))
title_lbl.pack(pady=20)


def begin():
    """Console compatibility (GUI uses buttons)."""
    print("Welcome to the flashcard game!")
    print("1. Start a new game")
    print("2. Load a saved game")


def full_deck():
    """Load deck from JSON file.

    Accepts either:
    - {"spanish_basic": [{"en":"hello","es":"hola"}, ...]}
    - or just a list: [{"en":"hello","es":"hola"}, ...]
    """
    with open("decks/spanish_basic.json", "r", encoding="utf-8") as f:
        return json.load(f)


def start_new_game(selected_deck, deck_name, initial_score: int = 0):
    if not selected_deck:
        messagebox.showerror("Error", "Selected deck was empty.")
        return

    game = GameBrain(selected_deck, deck_name)
    game.score = initial_score

    top = tk.Toplevel(root)
    top.title(f"Playing: {deck_name}")

    info = tk.Label(top, text=f"Deck '{deck_name}' loaded. {len(game.deck)} cards.", font=("Helvetica", 12))
    info.pack(padx=20, pady=(10, 0))

    spanish_var = tk.StringVar(value="")
    spanish_label = tk.Label(top, textvariable=spanish_var, font=("Helvetica", 14))
    spanish_label.pack(pady=(10, 5))

    entry = tk.Entry(top, width=40)
    entry.pack(pady=5)

    feedback_var = tk.StringVar(value="")
    feedback_label = tk.Label(top, textvariable=feedback_var, font=("Helvetica", 10))
    feedback_label.pack(pady=5)

    score_var = tk.StringVar(value=f"Score: {game.score}")
    score_label = tk.Label(top, textvariable=score_var, font=("Helvetica", 10))
    score_label.pack(pady=(5, 10))

    current_pair = [None]  # mutable container for closure

    def next_card():
        pair = game.pick_pair()
        current_pair[0] = pair
        if pair is None:
            spanish_var.set("No more cards — you're done!")
            entry.config(state="disabled")
            feedback_var.set(f"Final score: {game.score}")
            return
        spanish_var.set(pair.get("es", ""))
        entry.delete(0, tk.END)
        feedback_var.set("")
        entry.focus_set()

    def check_handler():
        pair = current_pair[0]
        if not pair:
            feedback_var.set("No card to check.")
            return
        user_input = entry.get()
        correct = game.check_answer(user_input, pair)
        score_var.set(f"Score: {game.score}")
        if correct:
            feedback_var.set("Correct — removed from deck.")
            next_card()
        else:
            feedback_var.set(f"Wrong — correct: {pair.get('en', '')}")

    def save_and_quit():
        save_name = simpledialog.askstring("Save Game", "Enter a name for your save file:")
        if not save_name:
            return
        path = game.save_game(save_name)
        messagebox.showinfo("Saved", f"Game saved to {path}")
        top.destroy()

    # Buttons
    btn_frame = tk.Frame(top)
    btn_frame.pack(pady=10)

    check_btn = tk.Button(btn_frame, text="Check", width=12, command=check_handler)
    check_btn.grid(row=0, column=0, padx=5)

    next_btn = tk.Button(btn_frame, text="Next", width=12, command=next_card)
    next_btn.grid(row=0, column=1, padx=5)

    save_btn = tk.Button(btn_frame, text="Save & Quit", width=12, command=save_and_quit)
    save_btn.grid(row=0, column=2, padx=5)

    # start first card
    next_card()


def on_new_game():
    """Prompt for deck name if the file is a dict of multiple decks."""
    full = full_deck()
    if isinstance(full, dict):
        keys = list(full.keys())
        hint = ", ".join(keys[:10]) + ("..." if len(keys) > 10 else "")
        deck_name = simpledialog.askstring("New Game", f"Enter the deck name to use (available: {hint}):")
        if not deck_name:
            return
        selected_deck = full.get(deck_name)
        if not selected_deck:
            messagebox.showerror("Error", f"Deck '{deck_name}' not found.")
            return
    else:
        selected_deck = full
        deck_name = "deck"

    messagebox.showinfo("New Game", f"Starting a new game with the {deck_name} deck!")
    start_new_game(selected_deck, deck_name)


def on_load_game():
    """Ask for a save filename and attempt to load it."""
    save_file = simpledialog.askstring("Load Game", "Enter the name of the save file to load:")
    if not save_file:
        return
    save_path = os.path.join("saves", f"{save_file}.json")
    if not os.path.exists(save_path):
        messagebox.showerror("Error", f"Save file '{save_file}' not found.")
        return

    with open(save_path, "r", encoding="utf-8") as f:
        reader_data = json.load(f)

    deck_to_use = None
    deck_name = None
    initial_score = 0

    if isinstance(reader_data, dict) and "remaining" in reader_data and "deck_name" in reader_data:
        deck_name = reader_data.get("deck_name")
        deck_to_use = reader_data.get("remaining")
        initial_score = reader_data.get("score", 0)
    else:
        if isinstance(reader_data, dict):
            keys = list(reader_data.keys())
            deck_name = keys[0] if keys else "deck"
            deck_to_use = reader_data.get(deck_name)
        else:
            deck_to_use = reader_data
            deck_name = deck_name or "deck"

    if not deck_to_use:
        messagebox.showerror("Error", "Loaded file did not contain a usable deck.")
        return

    messagebox.showinfo("Load Game", f"Loaded game data from {save_file}.")
    start_new_game(deck_to_use, deck_name, initial_score=initial_score)


# --- Root buttons ---
new_game_button = tk.Button(root, text="New Game", width=20, height=2, command=on_new_game)
new_game_button.pack(pady=10)
load_game_button = tk.Button(root, text="Load Game", width=20, height=2, command=on_load_game)
load_game_button.pack(pady=10)

# Optional console intro
begin()

# Main loop
root.mainloop()
