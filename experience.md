# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch ends with a mean progress of 0.1482 over 15 seeds (parent-eval.json). Deaths cluster into patterns:

- Xp11 deaths on Dlvl 1 from melee attrition (fast/strong monsters): seeds 1 (dwarf lord), 3 (fire ant), 5 (soldier ant), 6 (soldier ant), 9 (invisible Mordor orc) at progress ~0.2548.
- Xp10 deaths: seeds 0 (rothe Dlvl 1), 7 (poisoned by rotted rothe corpse Dlvl 3), 13 (dwarf lord Dlvl 5) at ~0.1791.
- Mid-low Xp on Dlvl 1/early: seed 8 (shattered potion Dlvl 1, Xp9, 0.117), seeds 2 and 14 (bolt of fire/cold Dlvl 1, Xp8, ~0.0745), seed 11 (pony Dlvl 4, Xp8, 0.0745).
- Very early deaths (food/latch-related): seed 12 (kobold lord Dlvl 2, Xp5, 0.0291), seed 10 (kitten Dlvl 2, Xp4, 0.0242), seed 4 (goblin Dlvl 2, Xp2, 0.0185).

## What is the problem

The wizard farms Dlvl 1 until Xp12 but rarely reaches Xp12; most games cap at Xp11 (0.2548) and die there to fast insects/lords in melee. Early deaths (seeds 4,10,12) occur when the bot descends to Dlvl 2 due to food/fainting issues and dies weak. The score cannot exceed Xp11 on Dlvl 1.

## What might solve it
See `experiments.md`.