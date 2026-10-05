# Next mutator experiment

Applied. The edit is one test on the fainting latch. Combat functions stay closed.

## Why it stopped

Run 37349624888 scored 0.09228385325013148. The parent is 0.11444300565928403. The mean falls by 0.022.

## What is the problem

The operator edited `fight2`. The tie-break left seed 4 at 2,742 turns and lowered seed 9 from Xp:11 to Xp:10. Earlier edits in `emergency_strategy` did the same kind of harm.

The kept gains are the corpse cap, the fainting latch, and the level-12 gate. Those edits are in `global_logic.py`. Seeds 4, 10, and 12 die at Xp:2, Xp:4, and Xp:5, on depth 2. The latch can send a fainting wizard downstairs before level 5.

## What might solve it

In `current_strategy`, the fainting test that sets `_xp_farm_level` to 2 also requires `experience_level >= 5`. Do not change `experience_level >= 12`. Do not edit `fight2` or `emergency_strategy`.

## Result

- iteration 1: 0.092 not kept (no-cell-improved). Decreases the mean by 0.022 (from 0.114 to 0.092). Seed 4 stayed at 2,742 turns. Seed 9 fell from 0.255 to 0.179.
