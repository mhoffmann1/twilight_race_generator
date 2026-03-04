#!/usr/bin/env python3
"""
TI4 faction pool generator (Base + PoK + Thunder combined])

- Input players: 3–6
- Each player gets exactly 5 factions.
- Across all players, every faction is used EXACTLY ONCE (30 total factions, 6*5=30).
- Constraints:
  - Each player gets at least 1 Prophecy of Kings (PoK) faction
  - Each player gets at least 1 Thunder faction
  - Remaining slots are filled with all Base factions + the one leftover PoK faction

Output:
  Player #X: <BASE64-encoded list of 5 factions, one per line>
"""

from __future__ import annotations

import argparse
import base64
import random
from typing import List, Dict


BASE = [
    "The Arborec",
    "The Barony of Letnev",
    "The Clan of Saar",
    "The Embers of Muaat",
    "The Emirates of Hacan",
    "The Federation of Sol",
    "The Ghosts of Creuss",
    "The L1Z1X Mindnet",
    "The Mentak Coalition",
    "The Naalu Collective",
    "The Nekro Virus",
    "The Sardakk N’orr",
    "The Universities of Jol-Nar",
    "The Winnu",
    "The Xxcha Kingdom",
    "The Yin Brotherhood",
    "The Yssaril Tribes",
]

POK = [
    "The Argent Flight",
    "The Empyrean",
    "The Mahact Gene-Sorcerers",
    "The Naaz-Rokha Alliance",
    "The Nomad",
    "The Titans of Ul",
    "The Vuil’raith Cabal",
]

VT = [
    "The Council Keleres",
    "Last Bastion",
    "The Ral Nel Consortium",
    "The Deepwrought Scholarate",
    "The Crimson Rebellion",
    "The Firmament / The Obsidian",
]


def b64_lines(lines: List[str]) -> str:
    payload = "\n".join(lines).encode("utf-8")
    return base64.b64encode(payload).decode("ascii")


def generate_pools(players: int, seed: int | None = None) -> Dict[int, List[str]]:
    if not (3 <= players <= 6):
        raise ValueError("Players must be between 3 and 6")

    per_player = 5
    total_needed = players * per_player

    rng = random.Random(seed)

    base = BASE[:]
    pok = POK[:]
    vt = VT[:]

    rng.shuffle(base)
    rng.shuffle(pok)
    rng.shuffle(vt)

    pools: Dict[int, List[str]] = {p: [] for p in range(1, players + 1)}

    # Step 1: Assign one unique VT per player
    for p in range(1, players + 1):
        pools[p].append(vt[p - 1])

    # Step 2: Assign one unique PoK per player
    for p in range(1, players + 1):
        pools[p].append(pok[p - 1])

    # Remove used factions from global pools
    used = set()
    for pool in pools.values():
        used.update(pool)

    remaining_factions = [
        f for f in (BASE + POK + VT) if f not in used
    ]

    rng.shuffle(remaining_factions)

    # Step 3: Fill remaining slots uniquely
    idx = 0
    for p in range(1, players + 1):
        while len(pools[p]) < per_player:
            pools[p].append(remaining_factions[idx])
            idx += 1

    # Final validation
    all_used = []
    for p in pools:
        if len(set(pools[p])) != per_player:
            raise RuntimeError(f"Duplicate inside Player {p}")
        all_used.extend(pools[p])

    if len(all_used) != len(set(all_used)):
        raise RuntimeError("Global duplicates detected")

    return pools


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TI4 faction pools (3–6 players, no duplicates, base64 output)."
    )
    parser.add_argument("players", type=int, help="Number of players (3-6)")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed")

    args = parser.parse_args()

    pools = generate_pools(args.players, seed=args.seed)

    print(f"Players: {args.players} | Factions per player: 5")
    if args.seed is not None:
        print(f"Seed: {args.seed}")
    print()

    for p in range(1, args.players + 1):
        print(f"Player #{p}: {b64_lines(pools[p])}")


if __name__ == "__main__":
    main()