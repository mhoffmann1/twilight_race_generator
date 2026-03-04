#!/usr/bin/env python3
"""
TI4 faction pool generator (Base + PoK + Thunder combined])

- Input players: 3–8
- Pool size per player:
    K = min(5, 30 // players)   # 8 players => 3
- Output: "Player #X:" then BASE64-encoded pool (one faction per line)
"""

from __future__ import annotations

import argparse
import base64
import random
from typing import Dict, List


BASE: List[str] = [
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

POK: List[str] = [
    "The Argent Flight",
    "The Empyrean",
    "The Mahact Gene-Sorcerers",
    "The Naaz-Rokha Alliance",
    "The Nomad",
    "The Titans of Ul",
    "The Vuil’raith Cabal",
]

VIGIL: List[str] = [
    "The Council Keleres",
]

THUNDER: List[str] = [
    "Last Bastion",
    "The Ral Nel Consortium",
    "The Deepwrought Scholarate",
    "The Crimson Rebellion",
    "The Firmament / The Obsidian",
]

# Combined “one expansion” bucket per your request
VIGIL_THUNDER: List[str] = VIGIL + THUNDER


def _cycle_pick(order: List[str], idx: int) -> str:
    if not order:
        raise ValueError("Empty faction list")
    return order[idx % len(order)]


def _b64_lines(lines: List[str]) -> str:
    payload = "\n".join(lines).encode("utf-8")
    return base64.b64encode(payload).decode("ascii")


def generate_pools(players: int, seed: int | None = None) -> Dict[int, List[str]]:
    if not (3 <= players <= 8):
        raise ValueError("players must be between 3 and 8")

    total_factions = len(BASE) + len(POK) + len(VIGIL_THUNDER)
    k = min(5, total_factions // players) 
    if k < 2:
        raise RuntimeError("Pool size too small to satisfy constraints")

    rng = random.Random(seed)

    base_order = BASE[:]
    pok_order = POK[:]
    vt_order = VIGIL_THUNDER[:]

    rng.shuffle(base_order)
    rng.shuffle(pok_order)
    rng.shuffle(vt_order)

    pools: Dict[int, List[str]] = {}

    for p in range(1, players + 1):
        picks: List[str] = []

        picks.append(_cycle_pick(pok_order, p - 1))
        picks.append(_cycle_pick(vt_order, p - 1))

        need = k - len(picks)
        if need > 0:
            base_idx = (p - 1) * need
            while need > 0:
                cand = _cycle_pick(base_order, base_idx)
                base_idx += 1
                if cand not in picks:
                    picks.append(cand)
                    need -= 1

        # Final safety: ensure no duplicates in a pool; refill from Base if needed
        seen = set()
        deduped: List[str] = []
        for f in picks:
            if f not in seen:
                seen.add(f)
                deduped.append(f)
        picks = deduped

        while len(picks) < k:
            cand = _cycle_pick(base_order, rng.randrange(10_000_000))
            if cand not in picks:
                picks.append(cand)

        pools[p] = picks

    return pools


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate base64-encoded TI4 faction pools per player (PoK + [Vigil+Thunder] + Base)."
    )
    parser.add_argument("players", type=int, help="Number of players (3-8).")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed.")
    args = parser.parse_args()

    pools = generate_pools(args.players, seed=args.seed)

    total_factions = len(BASE) + len(POK) + len(VIGIL_THUNDER)
    k = min(5, total_factions // args.players)

    print(f"Players: {args.players} | Factions per player: {k}")
    if args.seed is not None:
        print(f"Seed: {args.seed}")
    print()

    for pnum in range(1, args.players + 1):
        print(f"Player #{pnum}: {_b64_lines(pools[pnum])}")


if __name__ == "__main__":
    main()