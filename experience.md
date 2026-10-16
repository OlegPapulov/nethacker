# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The 15 judged games all end on the first dungeon levels. Eight of them -- seeds
0, 1, 3, 5, 6, 7, 9, and 13 -- are long: they farm dungeon level 1 up to
experience level 10 or 11 and then die to a mid-dungeon monster in melee, with no
monster killed from range and no hit point restored except by the emergency
healing potion. The bot lost because the wizard's spell advantage is only half
used.

The ends the judge already played:

| Seed | Milestone | Progress | Depth | Cause of death |
| ---- | --------- | -------- | ----- | -------------- |
| 0  | Xp:10 | 0.1791 | 1 | killed by a rothe |
| 1  | Xp:11 | 0.2548 | 1 | killed by a dwarf lord |
| 2  | Xp:8  | 0.0745 | 1 | killed by a bolt of fire |
| 3  | Xp:11 | 0.2548 | 1 | killed by a fire ant |
| 4  | Xp:2  | 0.0185 | 2 | killed by a goblin |
| 5  | Xp:11 | 0.2548 | 1 | killed by a soldier ant |
| 6  | Xp:11 | 0.2548 | 1 | killed by a soldier ant |
| 7  | Xp:10 | 0.1791 | 3 | poisoned by a rotted rothe corpse |
| 8  | Xp:9  | 0.1170 | 1 | killed by a shattered potion |
| 9  | Xp:11 | 0.2548 | 3 | killed by an invisible Mordor orc |
| 10 | Xp:4  | 0.0242 | 2 | killed by a kitten |
| 11 | Xp:8  | 0.0745 | 4 | killed by a pony |
| 12 | Xp:5  | 0.0291 | 2 | killed by a kobold lord |
| 13 | Xp:10 | 0.1791 | 5 | killed by a dwarf lord |
| 14 | Xp:8  | 0.0745 | 1 | killed by a bolt of cold |

Mean: 0.148248.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game
reaches. The long games plateau at experience level 10 or 11 because the wizard
has no way to keep its hit points up while it fights, and the short games die
early to food, traps, and weak monsters.

## What might solve it

See `experiments.md`: the second starting spellbook is a healing spell the agent
never re-learns and never casts. Keeping it memorized and casting it when hurt is
an unlisted action that can carry a long game to the next experience level.
