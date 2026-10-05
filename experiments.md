# Next mutator experiment

Applied. `emergency_strategy` stays closed. The edit is melee in `fight2` when a monster is adjacent.

## Why it stopped

Run 37337111283 scored 0.084 and then 0.074. The parent is 0.114. The hub read timed out after the second score. Neither child was kept.

## What is the problem

Both edits are in `emergency_strategy`, and that function runs before `fight2`. The search of up to 25 turns raised seed 4 and lowered seed 9 from Xp:11 to Xp:10. The step away left seed 4 at 2,742 turns and lowered seed 3 from 0.179 to 0.021.

## What might solve it

Do not edit `emergency_strategy`. Do not add `search`, `move`, `engrave`, or a loop there. In `fight2`, when a monster is adjacent, the action is melee. Do not call `search` in that case. Do not call `move` in that case.

Leave `fight_heur.py` forbidden. Leave the level-12 gate, the food latch, and the corpse cap. Leave the commented rest loop in place.

## Result

- iteration 1: 0.084 not kept (no-cell-improved). Decreases the mean by 0.031 (from 0.114 to 0.084). Added a search of up to 25 turns. Seed 4 rose from 0.018 to 0.029. Seed 9 fell from 0.255 to 0.179.
- iteration 2: 0.074 not kept (no-cell-improved). Decreases the mean by 0.040 (from 0.114 to 0.074). Stepped away below one third hit points. Seed 4 stayed at 2,742 turns. Seed 3 fell from 0.179 to 0.021. The hub read timed out.
