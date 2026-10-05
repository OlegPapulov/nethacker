# Next mutator experiment

Applied. The fainting latch stays unchanged. At experience level 11 the farm target is dungeon level 2.

## Why it stopped

Run 37355608122 scored 0.10209517981729713. The parent is 0.11444300565928403. The mean falls by 0.012.

## What is the problem

The operator added `experience_level >= 5` to the fainting latch. Seed 4 stayed at Xp:2. Seed 9 fell from Xp:11 to Xp:8. The early descent is how seed 9 reaches Xp:11.

## What might solve it

Leave the fainting test as hunger fainting and no edible corpse in reach. Do not add a level test to that line. After that test, when `experience_level >= 11`, set `level` to dungeon level 2. Seed 9 dies on depth 3.

Leave `fight2` and `emergency_strategy` closed. Leave the level-12 gate and the corpse cap.

## Result

- iteration 1: 0.102 not kept (no-cell-improved). Decreases the mean by 0.012 (from 0.114 to 0.102). Seed 4 stayed at 0.018. Seed 9 fell from 0.255 to 0.075.
