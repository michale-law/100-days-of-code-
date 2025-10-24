import csv, json, os

# Path to your CSV file
csv_path = os.path.join("decks", "spanish_basic.csv")
json_path = os.path.join("decks", "spanish_basic.json")

pairs = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Each row is a dict like {'en': 'house', 'es': 'casa'}
        pairs.append({"en": row["en"], "es": row["es"]})

deck = {
    "deck_name": "Spanish Basics",
    "pairs": pairs
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(deck, f, ensure_ascii=False, indent=2)

print(f"✅ Converted {csv_path} → {json_path}")
