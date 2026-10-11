# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note; the judge plays its 15 seeds on the tree I exit with. Local runs with arbitrary `make_environment`/`TrajectorySpec` seeds (same bot, same env interface, not the judge seeds) end mostly before Xp:10:

- Starvation deaths on the exhausted Doom floor: the wizard sits locked in `fight2` (Elbereth wait stand-off, HP 15-21) while hunger drops WEAK→FAINTING, with an edible non-rotting lichen corpse inside the 20-square corpse reach that is never eaten, then it walks for the down staircase at FAINTING and is killed (e.g. `killed by a bat`, `t=7383`; `died of starvation`, depth 2).
- Early melee attrition: low-Xp seeds die to coyote/hobgoblin/giant rat/rothe/gray ooze after repeated fights at low HP with no healing and a dagger as the only weapon.
- Random early traps: `killed by a falling rock` at turn 412; a lone `bolt of fire`; fainting mid-march into a fast monster.
- The runs that bank Xp:10 reproduce the parent exactly (turn-for-turn identical) and confirm the score-raising paths (stay to Xp:12, dlvl-2 latch, force bolt from Xp:10/dlvl-1, skill points into the wielded dagger) fire without regression.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches. Most seeds stall below Xp:10, so small survival gains that push one starving run from Xp:5-7 into Xp:10+=0.179 move the mean.

## What might solve it

See `experiments.md`. The submitted change is a rewrite of one function, `Agent.fight2` (`autoascend/agent.py`), which lets a WEAK/FAINTING wizard locked in a fight use the existing corpse-search reach to eat instead of waiting and then marching to certain death at the staircase.
