"""Summarise a trace: HP damage events, level timeline, and the final fight."""
from __future__ import annotations

import json
import sys
from collections import Counter

path = sys.argv[1]
rows = [json.loads(line) for line in open(path)]
self_glyph_fix = True

# drop the player's own tile from the monster list (the wizard glyph is the player)
for r in rows:
    pass

print(f"{len(rows)} rows, turns {rows[0]['t']}..{rows[-1]['t']}")

xl_at = {}
for r in rows:
    xl_at.setdefault(r["xl"], r["t"])
print("XL first reached at turn:", dict(sorted(xl_at.items())))

hp = [(r["t"], r["hp"], r["mhp"], r["en"], r["ac"], r["mons"]) for r in rows]
drops = []
for i in range(1, len(hp)):
    if hp[i][1] < hp[i - 1][1] and hp[i - 1][1] == hp[i - 1][2]:
        drops.append((hp[i - 1], hp[i], i))
print(f"\n{len(drops)} full-HP -> damaged transitions")
for prev, cur, i in drops[-8:]:
    print(f"  t={prev[0]:>6} {prev[1]}->{cur[1]} mons_before={prev[5]} mons_after={cur[5]}")

n = int(sys.argv[2]) if len(sys.argv) > 2 else 30
print(f"\nlast {n} rows (self glyph filtered):")
for r in rows[-n:]:
    mons = [m for m in r["mons"] if m[0] > 0]
    print(f"  t={r['t']:>6} {r['kind']:>6} hp={r['hp']:>2}/{r['mhp']:<3} en={r['en']:<3} ac={r['ac']} "
          f"xl={r['xl']} hng={r['hunger']} {r.get('mon') or ''} {mons}")
