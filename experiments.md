# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37145731075 scored 0.080 against a 0.077 parent. The child was kept. The operator did not edit `melee_monster_priority`.

## What is the problem

The gain is the `_xp_farm_level` latch. Seed 11 and seed 9 rose. Seed 13 fell. Seeds 4, 8, and 10 did not move. The depth-1 melee bonus is still in the file.

## What might solve it

The note leaves the 20-square corpse cap and `_xp_farm_level` in place. In `melee_monster_priority`, do not add 15 when `blstats.depth` is 1 and the monster is not in `INSECTS`. Every other file matches the parent. The operator writes the `# hypothesis:` comment and the line in `experiments.md` in ASD-STE100 style.

## Result

- iteration 1: 0.080 kept (registered). Increases the mean by 0.003 (from 0.077 to 0.080). Latched onto dungeon level 2 when fainting and no edible corpse was within 20 squares. The melee function did not change.
