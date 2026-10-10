# Playthrough

Identity: `wiz-hum-cha-mal` (wizard, chaotic, the parent batch).

## The games

15 seeds. Progress is the highest milestone a game reaches, either a dungeon level
(`Dlvl:N`) or an experience level (`Xp:N`). On these seeds the experience milestones
dominate: every seed's milestone is an `Xp:` value, because the wizard never descends
far enough for a `Dlvl:` value to beat its experience level.

| seed | milestone | progress | max depth | turns | cause of death |
|------|-----------|----------|-----------|-------|----------------|
| 0  | Xp:10 | 0.1791 | 2 | 56851 | killed by a giant bat |
| 1  | Xp:10 | 0.1791 | 1 | 46006 | killed by a killer bee |
| 2  | Xp:8  | 0.0745 | 1 | 34154 | killed by a bolt of fire |
| 3  | Xp:11 | 0.2548 | 1 | 69782 | killed by a spotted jelly |
| 4  | Xp:2  | 0.0185 | 2 |  2742 | killed by a goblin |
| 5  | Xp:10 | 0.1791 | 1 | 56808 | killed by a killer bee |
| 6  | Xp:11 | 0.2548 | 6 | 80609 | poisoned by a rotted hill orc corpse |
| 7  | Xp:10 | 0.1791 | 3 | 60316 | poisoned by a rotted rothe corpse |
| 8  | Xp:6  | 0.0369 | 1 |  9957 | killed by a newt |
| 9  | Xp:11 | 0.2548 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | Xp:4  | 0.0242 | 2 |  6313 | killed by a kitten |
| 11 | Xp:8  | 0.0745 | 4 | 23577 | killed by a pony |
| 12 | Xp:5  | 0.0291 | 2 |  5011 | killed by a kobold lord |
| 13 | Xp:10 | 0.1791 | 5 | 48694 | killed by a dwarf lord |
| 14 | Xp:8  | 0.0745 | 1 | 32018 | killed by a bolt of cold |

Mean progress: 0.1328.

## Why it stopped

Every run ends in death; none ascends. The long runs (seeds 3, 6, 9: ~70000-80000
turns, Xp:11) are the wizard farming the first Doom level. The short runs die early
in melee on the shallow levels. The batch's bottleneck is survival, and the deadliest
single mechanism is a lone fast or hard-hitting monster finishing a wizard that only
turns defensive once it is nearly dead.

The two highest-value runs that could have gone further, seeds 6 and 7, did not lose a
fight. They ate a **rotted** corpse and died of poison: "poisoned by a rotted hill orc
corpse" and "poisoned by a rotted rothe corpse". This is not a combat loss; it is the
wizard deliberately walking to food it has already decided is edible and then eating a
corpse that has since spoiled.

## What is the problem

Progress is the highest milestone a game reaches. The judge score is the mean of the 15
seeds. A child is kept only when that mean is strictly higher. Two of the three best runs
(seeds 6 and 7) end on a preventable poisoning, so a fix that keeps those runs alive --
or stops the wizard from ever feeding on a spoiled corpse on any seed -- is the highest
expected-value change.

## What might solve it

See `experiments.md`.
