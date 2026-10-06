# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

All 15 parent games ended in a death. None quit, none stalled, none hit the step cap (the largest is 128292 steps against 1000000). Mean progress 0.1144. One row per game, from `/refs/parent-eval.json`:

| game | milestone | progress | depth | turns | steps | death |
|---|---|---|---|---|---|---|
| 0 | Xp:9 | 0.1170 | 1 | 50145 | 70570 | poisoned by an orcish arrow |
| 1 | Xp:10 | 0.1791 | 1 | 46006 | 67619 | killed by a killer bee |
| 2 | Xp:8 | 0.0745 | 1 | 34154 | 47230 | killed by a bolt of fire |
| 3 | Xp:10 | 0.1791 | 3 | 57042 | 93017 | poisoned by an orcish arrow |
| 4 | Xp:2 | 0.0185 | 2 | 2742 | 2543 | killed by a goblin |
| 5 | Xp:10 | 0.1791 | 1 | 55705 | 89798 | killed by a giant bat |
| 6 | Xp:10 | 0.1791 | 3 | 73840 | 119722 | killed by a plains centaur |
| 7 | Xp:9 | 0.1170 | 6 | 34611 | 48345 | killed by a vampire bat |
| 8 | Xp:6 | 0.0369 | 1 | 9957 | 15857 | killed by a newt |
| 9 | Xp:11 | 0.2548 | 3 | 69906 | 128292 | killed by an invisible Mordor orc |
| 10 | Xp:4 | 0.0242 | 2 | 6313 | 7004 | killed by a kitten |
| 11 | Xp:8 | 0.0745 | 4 | 23577 | 30627 | killed by a pony |
| 12 | Xp:5 | 0.0291 | 2 | 5011 | 5286 | killed by a kobold lord |
| 13 | Xp:10 | 0.1791 | 5 | 48694 | 81225 | killed by a dwarf lord |
| 14 | Xp:8 | 0.0745 | 1 | 32018 | 43431 | killed by a bolt of cold |

Every milestone is an experience level. The deepest level any game reaches is Dlvl:6 (game 7), worth 0.035, less than the Xp:9 that game already banked, so on these 15 games only experience level moves the score. The farm gate keeps the wizard on Dungeons of Doom levels 1–2 for most of each game: nine of the fifteen die on depth 1–2, and the deepest death is depth 6.

## What is the problem

Combat ends every game; nothing else does. The deaths split three ways:

1. **Trading blows with an ordinary monster** — games 0, 3, 6, 9, 13 (orcish arrow ×2, plains centaur, invisible Mordor orc, dwarf lord) and games 2, 14 (bolts of fire and cold from a monster the wizard stood and fought). Seven games, all at Xp:8–11, worth 0.075–0.255 each. The test at `autoascend/combat/fight_heur.py:18` gives melee the +15 bonus whenever `hitpoints > 8`, so melee is worth 16 — more than any retreat the heatmap can offer one-on-one (the strongest is about +12: −9 on the tile the wizard stands on because the monster is adjacent, +3 on the ring two squares out). The wizard therefore keeps standing beside the monster until one of them falls, whatever its hit points are between 9 and its maximum. Emergency quaff only starts below a third of the maximum and prayer below a fifth (a sixth from experience level 6), and both need the right item or timing, so for most of the fight neither fires.
2. **Monsters listed as faster** — games 1, 5, 7, 10, 11 (killer bee, giant bat, vampire bat, kitten, pony). The `or is_monster_faster(...)` side of the same test keeps melee at 16 at any hit point total, by design: a faster monster hits us on every tile we move to, so running only collects free hits.
3. **Early levels and weak monsters** — games 4 (goblin, Xp:2), 12 (kobold lord, Xp:5), 8 (newt, Xp:6). At those levels the wizard's maximum hit points is near 16 or below, so any half-of-maximum threshold collapses back to the fixed 8. The newt is in `WEAK_MONSTERS`, which get no negative ring and a +2/+1 positive ring, so the wizard fights it to the death at any threshold.

The best game dies the same way as the worst: game 9 banks Xp:11 (0.2548), with Xp:12 at 0.3326 one level away, beside an invisible Mordor orc.

## What might solve it

See `experiments.md`.
