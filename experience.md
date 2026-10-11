# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The 15 judged games (parent batch) end as follows. Progress is the best
milestone ever banked; the score is the mean over the seeds.

| seed | progress | milestone | max depth | cause of death |
|------|----------|-----------|-----------|----------------|
| 0  | 0.1791 | Xp:10 | 4 | killed by a coyote |
| 1  | 0.2548 | Xp:11 | 1 | killed by a dwarf lord |
| 2  | 0.0745 | Xp:8  | 1 | killed by a bolt of fire |
| 3  | 0.2548 | Xp:11 | 1 | killed by a fire ant |
| 4  | 0.0185 | Xp:2  | 2 | killed by a goblin |
| 5  | 0.2548 | Xp:11 | 1 | killed by a soldier ant |
| 6  | 0.1791 | Xp:10 | 3 | killed by a hobbit |
| 7  | 0.1791 | Xp:10 | 3 | killed by a rotted rothe corpse (poison) |
| 8  | 0.0369 | Xp:6  | 1 | killed by a newt |
| 9  | 0.2548 | Xp:11 | 3 | killed by an invisible Mordor orc |
| 10 | 0.0242 | Xp:4  | 2 | killed by a kitten |
| 11 | 0.0745 | Xp:8  | 4 | killed by a pony |
| 12 | 0.0291 | Xp:5  | 2 | killed by a kobold lord |
| 13 | 0.1791 | Xp:10 | 5 | killed by a dwarf lord |
| 14 | 0.0745 | Xp:8  | 1 | killed by a bolt of cold |

The score is the mean of those seeds (about 0.1379).

## What is the problem

Every game is lost to a monster, and the four seeds that bank Xp:11 all die on
the first Doom level to a single dangerous monster (a dwarf lord, a fire ant, a
soldier ant, an invisible Mordor orc). The wizard has very few hit points and
its only ranged attack is force bolt (read off the farm floor); once a monster
reaches melee range the wizard trades blows and the fight is a coin flip.

The two ant deaths stand out. A fire ant and a soldier ant both move at speed 18
against the wizard's 12, so they are faster than the wizard. The bot's
`is_monster_faster` test is name-based and does not list the ants, so at low hit
points it drops the melee bonus for them and has the wizard try to walk away --
but a faster monster only follows and keeps attacking, so the wizard spends its
turns not dealing damage and dies. The four seeds that stay on a shallow floor
and keep eating reach Xp:11; the seeds that run out of food and drift down the
stairs die deeper (max depth 3-5) to the monsters there.

## What might solve it

See `experiments.md`.
