# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

Every game in the parent batch ends on the early dungeon levels, long before the
Amulet. The parent gets a wizard to `Xp:8`-`Xp:11` on dungeon level 1 and then
loses the wizard there. The 15 results are:

| seed | reached | level | where | end |
|------|---------|-------|-------|-----|
| 0 | Xp:10 | 4 | killed by a coyote |
| 1 | Xp:11 | 1 | killed by a dwarf lord |
| 2 | Xp:8  | 1 | killed by a bolt of fire |
| 3 | Xp:11 | 1 | killed by a fire ant |
| 4 | Xp:2  | 2 | killed by a goblin |
| 5 | Xp:11 | 1 | killed by a soldier ant |
| 6 | Xp:10 | 3 | killed by a hobbit |
| 7 | Xp:10 | 3 | poisoned by a rotted rothe corpse |
| 8 | Xp:9  | 1 | killed by a shattered potion |
| 9 | Xp:11 | 3 | killed by an invisible Mordor orc |
| 10 | Xp:4 | 2 | killed by a kitten |
| 11 | Xp:8 | 4 | killed by a pony |
| 12 | Xp:5 | 2 | killed by a kobold lord |
| 13 | Xp:10 | 5 | killed by a dwarf lord |
| 14 | Xp:8 | 1 | killed by a bolt of cold |

## What is the problem

The score is the mean of those seeds, `0.1432`. The bot stays on the first floor
until `Xp:12` and the food latch is what moves the farm one level down when the
wizard is fainting with no corpse in reach, so the short games (seeds 4, 10, 12)
are the food latch working as designed, not a mistake.

The deaths that are not an ordinary melee loss share one thing: seed 2, 8 and 14
end on dungeon level 1 on a **trap**. Seed 2 is killed by a bolt of fire and seed
14 by a bolt of cold; `GAME_RULES.md` names exactly this hazard on these floors -
"a bolt trap on these floors throws fire or cold" - and a shattered potion (seed
8) is the same fire blast setting off a carried potion. Those three games all die
while farming a floor the wizard had already cleared, at `Xp:8`-`Xp:9`, so the
wizard had to be routed onto the trap it had otherwise been avoiding.

The parent only avoids known traps while its search-stall window is shut. When
the search counts pile up (the wizard is stuck on a fully explored floor, which
is the normal state while farming dungeon level 1) the parent deliberately reopens
*every* trap to pathing for 50 turns. A fire or magic trap is then a legal tile
on the walk line, and one bolt ends the game.

## What might solve it

See `experiments.md`.
