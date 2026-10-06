# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

All fifteen games ended before the bot left the Dungeons of Doom. The bot's plan is
to stay on the first Doom level and farm experience until `experience_level >= 12`,
then take the stairs. Nobody reached 12. Every game ended while farming (or a few
steps after a latch to level 2/3), and the judge scored the highest milestone reached.

## What is the problem

Per-seed parents (milestone, progress, turns, max depth, death):

- 0  Xp:9  0.11705  50145t  depth 1  poisoned by an orcish arrow
- 1  Xp:10 0.17910  46006t  depth 1  killed by a killer bee
- 2  Xp:8  0.07454  34154t  depth 1  killed by a bolt of fire
- 3  Xp:10 0.17910  57042t  depth 3  poisoned by an orcish arrow
- 4  Xp:2  0.01848   2742t  depth 2  killed by a goblin
- 5  Xp:10 0.17910  55705t  depth 1  killed by a giant bat
- 6  Xp:10 0.17910  73840t  depth 3  killed by a plains centaur
- 7  Xp:9  0.11705  34611t  depth 6  killed by a vampire bat
- 8  Xp:6  0.03689   9957t  depth 1  killed by a newt
- 9  Xp:11 0.25480  69906t  depth 3  killed by an invisible Mordor orc
- 10 Xp:4  0.02416   6313t  depth 2  killed by a kitten
- 11 Xp:8  0.07454  23577t  depth 4  killed by a pony
- 12 Xp:5  0.02911   5011t  depth 2  killed by a kobold lord
- 13 Xp:10 0.17910  48694t  depth 5  killed by a dwarf lord
- 14 Xp:8  0.07454  32018t  depth 1  killed by a bolt of cold

Mean 0.11444300565928403.

Two shapes. The long games (0, 1, 3, 5, 6, 9, 13) burn tens of thousands of turns on
the early levels and die to ordinary melee or a bolt at Xp 9-11. The short games
(4, 8, 10, 12) die inside the first few thousand turns at Xp 2-6 - seed 4 to a goblin,
seed 8 to a *newt*, seed 10 to a kitten, seed 12 to a kobold lord. The wizard has very
few hit points, swings a quarterstaff, and has no reliable self-heal: once it has drunk
its starting potions it trades blows with whatever is next to it until it dies. Nothing
in the logs shows a god killing the bot, so the failures are lost hit points, not wrath.

## What might solve it

See `experiments.md`.