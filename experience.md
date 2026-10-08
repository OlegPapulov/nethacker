# Playthrough

Identity: `wiz-hum-cha-mal`

## The 15 games

The parent batch (mean 0.1144) is the baseline. All 15 seeds die (`end_status=1`)
with no stall, no quit, and no score above 0.2548.

| tid | progress | milestone | turns | depth | died by |
|-----|-----|-----|-----|-----|-----|
|  4 | 0.0185 | Xp:2  |  2,742 | 2 | a goblin |
| 10 | 0.0242 | Xp:4  |  6,313 | 2 | a kitten |
| 12 | 0.0291 | Xp:5  |  5,011 | 2 | a kobold lord |
|  8 | 0.0369 | Xp:6  |  9,957 | 1 | a newt |
|  2 | 0.0745 | Xp:8  | 34,154 | 1 | a bolt of fire |
| 11 | 0.0745 | Xp:8  | 23,577 | 4 | a pony |
| 14 | 0.0745 | Xp:8  | 32,018 | 1 | a bolt of cold |
|  0 | 0.1170 | Xp:9  | 50,145 | 1 | a poisoned orcish arrow |
|  7 | 0.1170 | Xp:9  | 34,611 | 6 | a vampire bat |
|  1 | 0.1791 | Xp:10 | 46,006 | 1 | a killer bee |
|  3 | 0.1791 | Xp:10 | 57,042 | 3 | a poisoned orcish arrow |
|  5 | 0.1791 | Xp:10 | 55,705 | 1 | a giant bat |
|  6 | 0.1791 | Xp:10 | 73,840 | 3 | a plains centaur |
| 13 | 0.1791 | Xp:10 | 48,694 | 5 | a dwarf lord |
|  9 | 0.2548 | Xp:11 | 69,906 | 3 | an invisible Mordor orc |

## Why it stops where it does

The wizard has no usable ranged attack and is weak in melee, so almost every run
lives and dies on the first So So Doom floor. It farms Doom floors until
experience level 12 (never reached; the runs cap at Xp 9-11 and push to depth
1-6 only when the store level latch or the stair cascade fires). Stay-level 10
costs 0.179, level 9 costs 0.117 and level 8 costs 0.0745.

## What kills it

- **Fast melee** (killer bee, giant bat, vampire bat): seeds 1, 5, 7. A fast
  monster acts before the wizard, so a few free hits end the run at Xp 9-10.
- **Ranged and poison** (orcish arrow x2, bolt of fire, bolt of cold, plains
  centaur): seeds 0, 2, 3, 6, 14. The archers and casters kill the wizard while
  the melee is a step behind.
- **Slow melee** (goblin, newt, kobold lord, dwarf lord, invisible Mordor orc):
  seeds 4, 8, 9, 12, 13. Weak fights that end early runs (tid 4 dies at turn
  2,742 with Xp:2) — the wizard fights with little life left and no healing
  potion identified.
- **"A kitten" and "a pony"** (seeds 10 and 11): these are the character's own
  pet and a peaceable herd animal. A pet or peaceful monster only becomes
  hostile if the wizard harms it. The wizard never *melees* pets or peaceful
  monsters — `get_visible_monsters` excludes both (`peaceful_monster_mask`,
  `G.PETS`) — so the only code path that hits them is the wand ray.

## The wand ray

The wizard starts carrying an identified `wand of cold (0:8)`, a bouncing ray
wand, so the fight code zaps it from turn one. `_simulate_wand_path` walks the
beam:
- a monster on the `monsters` list (hostile, visible) is a target,
- a pet glyph (`G.PETS`) is collateral worth `-20*probability` and stops nothing,
- a **peaceful** monster (`peaceful_monster_mask`) falls through to `None` and
  is charged **zero**, even though the beam hits it (range is still reduced).

The launcher code (`ranged_priority`) refuses to fire through any monster that
is not an intended target; the wand code has no such guard. A ray aimed down a
corridor or reflected off a wall passes through a neighbouring pony, horse or
unicorn with no cost at all, turning it hostile — and on tid 11 that peaceable
pony then killed the wizard, who cannot even fight back while the victim is
still flagged peaceful. Tid 10's "kitten" is the same mechanism on the pet:
`-20*probability` is enough to encumber the beam but not to forbid it, and a
hostile pet is never visible to the melee code, so every follow-up hit is free.

## What might solve it

Treat a peaceful monster in the beam exactly like a pet: count it as collateral
worth the same `-20*probability` penalty. This is the one test the wand path is
still missing — the launcher already refuses such shots and pets already carry
the cost. It removes the mechanism behind the two seeds the wizard otherwise
cannot fight, without adding an action. See `experiments.md`.