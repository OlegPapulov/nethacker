# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37169391861 was cancelled after six hours. Iteration 1 scored 0.114, the parent mean. The 15 seeds match the parent turn for turn. Iteration 2 has no score.

## What is the problem

The operator edited `ret -= 6`, the launcher penalty. The note asked for the 15-point bonus. A wizard rarely holds a ranged weapon, so the launcher line does not change the 15 games. Two iterations do not finish before the Actions job stops at 360 minutes.

## What might solve it

The note names the line `ret += 15` after `hitpoints > 8 or is_monster_faster`. When `blstats.depth` is 1 and the monster is not in `INSECTS`, that line does not add 15. Do not edit `ret -= 6`. That launcher change was scored. Leave `experience_level >= 12`, `_xp_farm_level`, and the 20-square corpse cap. The next run is one iteration.

## Result

- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Changed the launcher penalty. The 15 seeds match the parent.
- iteration 2: none. The job was cancelled at 360 minutes. No score.
