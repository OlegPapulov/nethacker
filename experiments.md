# Next mutator experiment

Applied with this change. The task is the commented Elbereth block in `emergency_strategy`. `fight_heur.py` is forbidden.

## Why it stopped

Run 37238643759 scored 0.079 and then 0.065. The parent is 0.114 both times. The checkout was the seed. The tie rule worked.

## What is the problem

The operator does not copy the block. The notes were rewritten, and the `ret += 15` lines stayed. Both trees insert a new bonus before `return ret`.

Iteration 1 adds monster difficulty and speed. Iteration 2 adds a melee roll against armor class when two monsters stand adjacent. Seeds 4, 10, and 12 keep the same turn counts. Seed 9 falls from Xp:11 in both iterations. The mean falls.

A paste of that block has failed in three forms. A named neighbor line gets edited. A prose rule becomes a different test. A copy order becomes an insert at the end of the function. The harness brief tells the operator to write one new idea. The operator does that.

The kept gains left this function alone. The corpse cap, the food latch, and the level-12 gate raised the mean. Edits inside `melee_monster_priority` have not.

## What might solve it

Do not ask the operator to paste the block again. Do not send another task into `melee_monster_priority`.

Write the depth-1 block into `autoascend/combat/fight_heur.py` on the checkout. Let `.github/workflows/score.yml` play the 15 seeds. Do not dispatch `mutate.yml` for that commit. The operator does not run, so it cannot replace the block.

Leave `experience_level >= 12`, `_xp_farm_level`, and the 20-square corpse cap.

## Result

- iteration 1: 0.079 not kept (no-cell-improved). Decreases the mean by 0.036 (from 0.114 to 0.079). Added a difficulty bonus before `return ret`. Seed 6 rose from 0.179 to 0.255. Seed 9 fell from 0.255 to 0.029. Seeds 4, 10, and 12 did not move.
- iteration 2: 0.065 not kept (no-cell-improved). Decreases the mean by 0.049 (from 0.114 to 0.065). Added an armor bonus before `return ret`. Seed 2 rose from 0.075 to 0.117. Seed 9 fell from 0.255 to 0.117. Seeds 4, 10, and 12 did not move.
