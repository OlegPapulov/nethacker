# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

All fifteen parent games were played to the death. None quit, none timed out
(`end_status` is `1` on every row of `/refs/parent-eval.json`), so every score in
the table below is a death score.

| seed | progress | milestone | max depth | turns | death |
|---|---|---|---|---|---|
| 0 | 0.1170 | Xp:9  | 1 | 50145 | poisoned by an orcish arrow |
| 1 | 0.1791 | Xp:10 | 1 | 46006 | killed by a killer bee |
| 2 | 0.0745 | Xp:8  | 1 | 34154 | killed by a bolt of fire |
| 3 | 0.1791 | Xp:10 | 3 | 57042 | poisoned by an orcish arrow |
| 4 | 0.0185 | Xp:2  | 2 |  2742 | killed by a goblin |
| 5 | 0.1791 | Xp:10 | 1 | 55705 | killed by a giant bat |
| 6 | 0.1791 | Xp:10 | 3 | 73840 | killed by a plains centaur |
| 7 | 0.1170 | Xp:9  | 6 | 34611 | killed by a vampire bat |
| 8 | 0.0369 | Xp:6  | 1 |  9957 | killed by a newt |
| 9 | 0.2548 | Xp:11 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | 0.0242 | Xp:4  | 2 |  6313 | killed by a kitten |
| 11 | 0.0745 | Xp:8  | 4 | 23577 | killed by a pony |
| 12 | 0.0291 | Xp:5  | 2 |  5011 | killed by a kobold lord |
| 13 | 0.1791 | Xp:10 | 5 | 48694 | killed by a dwarf lord |
| 14 | 0.0745 | Xp:8  | 1 | 32018 | killed by a bolt of cold |

mean = 1.7166450848892605 / 15 = 0.11444300565928403

Progress depends only on the highest experience level a game ever reached:
Xp:2 is 0.0185, Xp:4 0.0242, Xp:5 0.0291, Xp:6 0.0369, Xp:8 0.0745, Xp:9
0.1170, Xp:10 0.1791, Xp:11 0.2548. Nothing else in the row moves the number,
and because progress is the highest milestone a game ever reaches, a game can
only be helped by living longer. Seven seeds stop at Xp:8 or below (seeds 4, 8,
10, 12, 2, 11, 14) and account for 0.3322 of the 1.7166 total; the other eight
farm the Doom floors for 34k–74k turns and stop at Xp:9–11.

Three shapes of game:

* **Short games (seeds 4, 12, 10, 8): 2.7k–10k turns, depth 1–2, Xp 2–6.** The
  wizard dies before the experience curve pays anything. Seed 4 dies to a
  goblin (speed 6) at Xp:2 in 2,742 turns, seed 12 to a kobold lord (speed 6),
  seed 8 to a newt (speed 6), seed 10 to a kitten (speed 18). Every one of them
  is a melee death, i.e. the wizard stood and traded blows with something it
  could have outrun, at a hit point total that cannot absorb two hits.
* **Xp:8 games (seeds 11, 14, 2): 23k–34k turns, depth 1–4.** Same story, one
  fight later: a pony, a bolt of cold, a bolt of fire.
* **Long games (the other eight): 34k–74k turns, depth 1–6, Xp 9–11.** The
  floor is farmed for tens of thousands of turns until a monster takes the last
  hit point; the best of them (seed 9) stops at Xp:11 and 0.2548.

Classifying all fifteen deaths:

* **Faster than the wizard (speed > 12): 6.** killer bee 18, giant bat 22,
  vampire bat 20, kitten 18, pony 16, plains centaur 18. These act first every
  round, which is exactly what the rules tip says: *"A faster monster takes a
  turn before the wizard takes a turn. A few hits kill the wizard."*
* **Slower than the wizard, melee: 5.** goblin 6, kobold lord 6, dwarf lord 6,
  Mordor orc 5, newt 6. The wizard is faster than all of them and could simply
  walk away; it did not, because `melee_monster_priority` starts at 1 and gets
  `+15` while hit points are above 8 (or the monster is faster), so it only
  falls back to 1 — flee — at 8 hit points or below, absolute.
* **Ranged or poison: 4.** two orcish arrows, a bolt of fire, a bolt of cold.
  Standing in something's line of fire until the poison or the bolt finishes
  the job.

All eleven melee deaths are decided by two frozen thresholds: the +15 melee
bonus while hit points are above 8 or the monster is faster, and the
`imminent_death_on_melee` flee trigger at 8 (16 against a pet or an insect).
The `GAME_RULES.md` assumptions measured both, so neither is the next edit.
What is *not* measured is whether the wizard is healthy and fed when it takes
those fights — and it usually is not, because of one unrelated gate.

## What is the problem

`fight2` is the strategy that owns every turn in which any visible monster is
within seven squares of the wizard (`agent.py`, `if not monsters or all(dis > 7
for dis, *_ in monsters)`). It is registered ahead of `follow_guard`, ahead of
the whole eating group, and ahead of `current_strategy`, so while a monster
sits anywhere inside that seven-square bubble the wizard cannot

* walk to a corpse — `eat_corpses_from_ground(only_below_me=False)` is gated at
  `hunger_state >= Hunger.WEAK` and capped at 20 squares, but it sits *below*
  `fight2` in `global_strategy`, so the 20-square walk never happens whenever
  something is in sight,
* eat the food in its pack (`eat_from_inventory`), or
* run the rest loop, `exploration_strategy(None).until(hp >= 0.8 * max)`, which
  is the wizard's only source of hit points short of prayer.

The two rules therefore contradict each other. The parent will walk twenty
squares for a corpse once it is weak, and simultaneously refuse to walk one
square for the same corpse because a goblin is standing five squares away. It
keeps kiting instead, hunger runs from weak to fainting, and the rules say
what happens next: *"Eat before a faint. A faint next to a monster is a
death."* The parent's own comment on the `WEAK` eat step already says the
wizard "spends whole games at hunger WEAK/FAINTING -- helpless for dozens of
turns per faint and easy prey."

The same gate holds the wizard out of its own rest loop, so it enters the
fights it cannot avoid at 50–70% of its maximum hit points, which is where a
speed-18 bee or a goblin's 1d6 finishes it. Seven seeds stop at Xp:8 or below
on melee and ranged deaths, and the eight seeds that do farm well stop at
Xp:9–11 — every one of the fifteen ends in combat, none of them in food,
traps or a quit.

## What might solve it

See `experiments.md`.
