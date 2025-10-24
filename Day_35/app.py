# imports we need for our app
import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import json
import os

root = tk.Tk()
root.title("Flashcard Game")
Spanish_card_Match = tk.Label(root, text="Spanish Card Match", font=("Helvetica", 16))
Spanish_card_Match.pack(pady=20)


def on_new_game():
    """Handler for New Game button. Asks for a deck name via dialog and starts the game."""
    Full_deck = full_deck()
    deck_name = simpledialog.askstring("New Game", "Enter the deck name you want to use:")
    if not deck_name:
        return
    selected_deck = Full_deck.get(deck_name)
    if not selected_deck:
        messagebox.showerror("Error", f"Deck '{deck_name}' not found.")
        return
    messagebox.showinfo("New Game", f"Starting a new game with the {deck_name} deck!")
    start_new_game(selected_deck, deck_name)


def on_load_game():
    """Handler for Load Game button. Asks for a save filename and attempts to load it."""
    save_file = simpledialog.askstring("Load Game", "Enter the name of the save file to load:")
    if not save_file:
        return
    save_path = f"saves/{save_file}.json"
    if not os.path.exists(save_path):
        messagebox.showerror("Error", f"Save file '{save_file}' not found.")
        return
    with open(save_path, "r", encoding="utf-8") as f:
        reader_data = json.load(f)
    messagebox.showinfo("Load Game", f"Loaded game data from {save_file}.")


new_game_button = tk.Button(root, text="New Game", width=20, height=2, command=on_new_game)
new_game_button.pack(pady=10)
load_game_button = tk.Button(root, text="Load Game", width=20, height=2, command=on_load_game)
load_game_button.pack(pady=10)







# once program starts we will run this function
def begin():
    # kept for compatibility with any console-based flows; GUI uses buttons
    print("Welcome to the flashcard game!")
    print("1. Start a new game")
    print("2. Load a saved game")


def full_deck():
    with open("decks/spanish_basic.json", "r", encoding="utf-8") as f:
        Full_deck = json.load(f)
    return Full_deck


def start_new_game(selected_deck, deck_name):
    """Minimal GUI-based starter for a new game: opens a window with deck info.

    This is a small placeholder to show the deck loaded. You can expand this to
    show cards, handle answers, scoring, etc.
    """
    if not selected_deck:
        return
    top = tk.Toplevel(root)
    top.title(f"Playing: {deck_name}")
    try:
        count = len(selected_deck)
    except TypeError:
        count = 1
    info = tk.Label(top, text=f"Deck '{deck_name}' loaded. {count} cards.", font=("Helvetica", 12))
    info.pack(padx=20, pady=20)


root.mainloop()