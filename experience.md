# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The end of each of the 15 recorded games (parent batch), by seed:

| seed | milestone | progress | turns | depth | end |
|---:|:--|--:|--:|--:|---|
| 0 | Xp:10 | 0.1791 | 56851 | 2 | killed by a giant bat |
| 1 | Xp:10 | 0.1791 | 46006 | 1 | killed by a killer bee |
| 2 | Xp:8 | 0.0745 | 34154 | 1 | killed by a bolt of fire |
| 3 | Xp:11 | 0.2548 | 69782 | 1 | killed by a spotted jelly |
| 4 | Xp:2 | 0.0185 | 2742 | 2 | killed by a goblin |
| 5 | Xp:10 | 0.1791 | 56808 | 1 | killed by a killer bee |
| 6 | Xp:11 | 0.2548 | 81066 | 6 | killed by a housecat |
| 7 | Xp:10 | 0.1791 | 60316 | 3 | poisoned by a rotted rothe corpse |
| 8 | Xp:6 | 0.0369 | 9957 | 1 | killed by a newt |
| 9 | Xp:11 | 0.2548 | 69906 | 3 | killed by an invisible Mordor orc |
| 10 | Xp:4 | 0.0242 | 6313 | 2 | killed by a kitten |
| 11 | Xp:8 | 0.0745 | 23577 | 4 | killed by a pony |
| 12 | Xp:5 | 0.0291 | 5011 | 2 | killed by a kobold lord |
| 13 | Xp:10 | 0.1791 | 48694 | 5 | killed by a dwarf lord |
| 14 | Xp:8 | 0.0745 | 32018 | 1 | killed by a bolt of cold |

## What is the problem

Most games stop between Xp:4 and Xp:11. Small monsters reach the wizard and
hit a low-hit-point caster (giant bat, killer bee, newt, kitten, goblin,
kobold lord, pony). At Xp:10-11 on the first level the wizard is farming and
has one ranged attack, force bolt, but it never actually fires: the spell was
memorized from the starting book at turn ~0, a memorized spell lapses ~20,000
turns after it is learned, the farm floor only begins at Xp>=10 (turn 38k+ in
seed 3), and every cast there is refused with "Your knowledge of this spell is
twisted", which stuns instead of firing. The killer-bee deaths on seeds 1 and
5 are exactly that: a bee that a working force bolt kills at range instead
reaches the caster and kills it. A few games also poison themselves on rotted
corpses (seed 7) or die to generic ranged bolts.

## What might solve it

At the start of the farm floor, re-learn force bolt from the dropped starting
spellbook so the accumulated ranged-attack code actually fires, turning the
Xp:10-11 killer-bee/two-squares deaths into ranged kills. See
`experiments.md`.
