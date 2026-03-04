# Twilight Imperium 4E – Faction Pool Generator v1.1

This script generates **private faction pools** for each player in a game of Twilight Imperium 4th Edition  
(Base Game + Prophecy of Kings + Thunder’s Edge).

Each player receives a **BASE64-encoded list of factions**, so they can privately decode their available options without revealing them immediately.

---

## Features

- Supports **3–6 players**
- Each player receives:
  - At least **1 faction from Prophecy of Kings**
  - At least **1 faction from Vigil/Thunder’s Edge (combined)**
  - Remaining factions from the **Base Game**
- Each player gets 5 races to pick from
- Output is **BASE64 encoded** for fun “hidden pool” sharing

---

## Requirements

- Python 3.8+
- No external dependencies

---

## Usage

Run the script from the command line:

```bash
python3 shuffle_races.py <number_of_players>
```

Example:

```bash
python3 shuffle_races.py 6
```

Optional reproducible seed:

```bash
python3 shuffle_races.py 8 --seed 42
```

---

## Example Output

```
Players: 6 | Factions per player: 5

Player #1: VGhlIEFyYm9yZWMKVGhlIE1haGFjdCBHZW5lLVNvcmNlcmVycwpUaGUgQXJnZW50IEZsaWdodApUaGUg...
Player #2: VGhlIFdpbm51ClRoZSBUaXRhbnMgb2YgVWwKVGhlIEVtcHlyZWFuClRoZS...
```

Each line after `Player #X:` is a BASE64-encoded list of factions (one faction per line).

---

# Instructions for Players

When the organizer posts the output:

1. Find your player number (e.g., **Player #3**).
2. Copy your BASE64 string.

---

## To Decode Your Pool

Use this website: https://emn178.github.io/online-tools/base64_decode.html

1. Paste your BASE64 string into the input box.
2. Click **Decode**.
3. You will see your faction pool.

---

## After You Choose a Faction

To secretly submit your chosen faction:

1. Copy the **exact faction name**
2. Encode it using: https://emn178.github.io/online-tools/base64_encode.html
3. Send the encoded result to the group chat.

Everyone can then decode simultaneously for dramatic reveal.

---

## Notes

- BASE64 is **not secure** — anyone can decode anyone else's pool.
- This is just for fun and to avoid accidental spoilers.
- Within a single player's pool, there are no duplicates.

---

## Enjoy the Draft!

May your trade goods be plentiful and your neighbors peaceful.
