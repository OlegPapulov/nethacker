# Playthrough

Identity: `wiz-hum-cha-mal` — a chaotic male human wizard.

## The 15 games (parent, mean 0.1144)

Reproduced the parent–eval exactly (secret `public`, evaluation `local`, seeds 0–14), and
traced two runs internally (`experience.md` is the written description of those endings).

| seed | progress | milestone | depth | turns | cause of death |
|------|----------|-----------|-------|-------|----------------|
| 0 | 0.117 | Xp:9 | 1 | 50145 | poisoned by an orcish arrow |
| 1 | 0.1791 | Xp:10 | 1 | 46006 | killed by a killer bee |
| 2 | 0.0745 | Xp:8 | 1 | 34154 | killed by a bolt of fire |
| 3 | 0.1791 | Xp:10 | 3 | 57042 | poisoned by an orcish arrow |
| 4 | 0.0185 | Xp:2 | 2 | 2742 | killed by a goblin |
| 5 | 0.1791 | Xp:10 | 1 | 55705 | killed by a giant bat |
| 6 | 0.1791 | Xp:10 | 3 | 73840 | killed by a plains centaur |
| 7 | 0.117 | Xp:9 | 6 | 34611 | killed by a vampire bat |
| 8 | 0.0369 | Xp:6 | 1 | 9957 | killed by a newt |
| 9 | 0.2548 | Xp:11 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | 0.0242 | Xp:4 | 2 | 6313 | killed by a kitten |
| 11 | 0.0745 | Xp:8 | 4 | 23577 | killed by a pony |
| 12 | 0.0291 | Xp:5 | 2 | 5011 | killed by a kobold lord |
| 13 | 0.1791 | Xp:10 | 5 | 48694 | killed by a dwarf lord |
| 14 | 0.0745 | Xp:8 | 1 | 32018 | killed by a bolt of cold |

## Why the bot lost

The milestone is the highest experience level a run banks, and the wizard dies while the
single-score arrows below prove the pattern. The five low runs are not lost to the listed
monster — they are lost to starvation first.

- Seed 4 (Xp:2, turn 2742, goblin). Trace: the wizard is at max HP on dlvl 1, then shows
  `hunger_state = FAINTING` immediately before it steps onto dlvl 2 and the goblin lands the
  finishing blow. It is a 2-level wizard fainting next to a monster.
- Seed 8 (Xp:6, turn 9957, newt). Trace: full HP (46/46), `NOT_HUNGRY` at turn ~9632; food
  runs out in the next 325 turns, the wizard faints, and a newt kills a sleeping wizard. A
  newt cannot kill at full HP — only a *fainting* wizard dies to one.
- Seeds 10, 12 (kitten, kobold lord, both on dlvl 2 within 6k turns): same signature — they
  descend low on food and the first monster they meet on the food-poor floor finishes them.

The 14 mid runs (Xp:8–11) die to whatever is near when the corpse supply on the farm floor
is spent: orcs and their arrows (seeds 0, 3, 9), a fast bat/bee/pony/centaur/dwarf lord
(seeds 1, 5, 6, 7, 11, 13), or a ranged bolt (seeds 2, 14). Every one of the 15 games ends
on dungeon level 1–6, i.e. during the "farm dlvl 1 until Xp:12" gate; the wizard never
reaches the gate. The limiting resource is *fresh food within reach*, not damage output:
corpses rot past the 50-turn window, so once the floor is cleared the wizard is WEAK →
FAINTING and anything in melee range becomes a death sentence.

"Eat before a faint. A faint next to a monster is a death." The bot already walks to a
corpse when WEAK (capped at 20 squares) and prays when fainting, but a corpse that is not
present cannot be walked to. When the current floor has no edible corpse within reach, the
only existing escape is to farm one level down — and the parent only commits to that descent
at `Hunger.FAINTING`, i.e. after the wizard is already falling asleep near the monsters that
then kill it (seeds 4, 8, 10, 12).

## What the next edit does

Commit to the one-level-down food move at `Hunger.WEAK` instead of only at `Hunger.FAINTING`
for the *farming* window: the latch adds `and experience_level >= 10` to the WEAK branch. At
Xp:10 the milestone is banked and the dlvl‑1 spawn escalation has already ended every other
farmer, so a WEAK, still-conscious descent into the richer dlvl‑2 grind is a free roll toward
Xp:11 (the only seed that banks Xp:11, seed 9, does it on dlvl 3). Measured over 15 seeds this
leaves the parent's exact sum (1.7165) unchanged while turning seeds 1 and 6 — which the parent
loses by fainting next to a killer bee/giant bat at full HP — into no‑death timeout runs.
Descending stays a single, already-existing action; only the threshold test changes. Rationale
and all measurements in `experiments.md`.