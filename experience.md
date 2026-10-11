# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

Every game ended in death; the 15 parent seeds ended as follows (milestone = highest
experience level reached):

- seed 0: Xp:10, dungeon level 2, killed by a giant bat.
- seed 1: Xp:10, level 1, killed by a killer bee.
- seed 2: Xp:8, level 1, killed by a bolt of fire.
- seed 3: Xp:11, level 1, killed by a spotted jelly.
- seed 4: Xp:2, level 2, killed by a goblin.
- seed 5: Xp:10, level 1, killed by a killer bee.
- seed 6: Xp:11, level 6, killed by a housecat.
- seed 7: Xp:10, level 3, poisoned by a rotted rothe corpse.
- seed 8: Xp:6, level 1, killed by a newt.
- seed 9: Xp:11, level 3, killed by an invisible Mordor orc.
- seed 10: Xp:4, level 2, killed by a kitten.
- seed 11: Xp:8, level 4, killed by a pony.
- seed 12: Xp:5, level 2, killed by a kobold lord.
- seed 13: Xp:10, level 5, killed by a dwarf lord.
- seed 14: Xp:8, level 1, killed by a bolt of cold.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.
Experience level is the milestone on every seed, so the mean is dragged down by the two
games that stall at Xp:2 and Xp:4, and by the many games that reach Xp:8..Xp:11 and then
die to a melee monster before reaching Xp:12. The dominant late deaths are melee (giant
bat, killer bee, spotted jelly, housecat, Mordor orc, dwarf lord) on or near the farming
floor. The bot reaches Xp:10+, then runs out of thrown ammo and trades blows, dying
before Xp:12.

## What might solve it

See `experiments.md`.
