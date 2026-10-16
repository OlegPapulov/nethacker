# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The judge already played these 15 games; their ends are the rows below.

| seed | milestone | depth | turns | how it ended |
|------|-----------|-------|-------|--------------|
| 0 | Xp:10 | 1 | 56188 | killed by a rothe |
| 1 | Xp:11 | 1 | 66905 | killed by a dwarf lord |
| 2 | Xp:8  | 1 | 34154 | killed by a bolt of fire |
| 3 | Xp:11 | 1 | 60050 | killed by a fire ant |
| 4 | Xp:2  | 2 | 2742  | killed by a goblin |
| 5 | Xp:11 | 1 | 92000 | killed by a soldier ant |
| 6 | Xp:11 | 1 | 73088 | killed by a soldier ant |
| 7 | Xp:10 | 3 | 60316 | poisoned by a rotted rothe corpse |
| 8 | Xp:9  | 1 | 35235 | killed by a shattered potion |
| 9 | Xp:11 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | Xp:4 | 2 | 6313  | killed by a kitten |
| 11 | Xp:8 | 4 | 23577 | killed by a pony |
| 12 | Xp:5 | 2 | 5011  | killed by a kobold lord |
| 13 | Xp:10 | 5 | 48694 | killed by a dwarf lord |
| 14 | Xp:8 | 1 | 32018 | killed by a bolt of cold |

The mean is 0.1482. The wizard banks experience level 10-11 on the first Doom
floors and then dies to a single strong monster, or to a group that walks up and
hits it several times in one turn. Nine of the fifteen games end that way (seeds
0, 1, 3, 5, 6, 9, 11, 13 plus the pony on seed 11), and the five longest games
all stop at experience level 11 against a soldier ant, a fire ant, a dwarf lord,
a rothe, or a Mordor orc. The rest end to a bouncing ray, a shattered potion, a
rotted corpse, or an early monster on the floors below the farm.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game
reaches. The wizard has no ranged answer once a strong monster closes, so it
walks into melee in an open room and trades blows with everything the room can
reach it with.

## What might solve it

See `experiments.md`.
