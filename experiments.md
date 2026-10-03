# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37133701364 scored 0.040 against a 0.077 parent. The operator cut search. The operator did not edit `melee_monster_priority`.

## What is the problem

`_keep_win` still omits `exploration_logic.py`. That paragraph is the task. The header ban is not what the last operator followed.

The melee condition is also wrong for the five short games. A coyote, a kobold zombie, and a newt receive the extra 15 only when hit points are above 8. `imminent_death_on_melee` becomes true for them at 8 or below, after the 15 is already gone. A soldier ant is in `INSECTS`, so the same check is true at 16 hit points. The instruction would change those long fights and would miss three short games.

## What might solve it

In `melee_monster_priority`, do not add 15 when `blstats.depth` is 1 and the monster is not in `INSECTS`. A bat, a coyote, a kobold zombie, and a newt lose the bonus on depth 1. A soldier ant, a fire ant, and a giant beetle keep it. Deeper levels keep the current bonus. Do not edit `exploration_logic.py`. Every other file matches the parent. The search tree already scored 0.040.

## Result

- iteration 1: 0.040 not kept (no-cell-improved). Decreases the mean by 0.037 (from 0.077 to 0.040). Visited unseen tiles before a search. Seeds 10 and 12 rose. Seed 13 fell from 0.179 to 0.024.
