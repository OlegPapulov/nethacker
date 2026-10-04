# Next mutator experiment

Applied with this change. A tie keeps the checkout. The seed says to copy the second block and names no other condition.

## Why it stopped

Run 37233060279 scored 0.08065773574577405 against a 0.114 parent. The tree is `43076a3`. The parent seed is `524d774`.

## What is the problem

`best_public` uses `>`. A tie keeps the first hub row. That row was `524d774`, an unkept tree with the same 0.114 score as the checkout. The run then edited that tree, not the kept bot.

The task showed the exact depth-1 block. The task also said "do not add 15". The operator wrote a different test: monster difficulty at most the experience level, and 21 when the monster has no difficulty. Versus `524d774`, that test is the only new code.

Seed 8 rose from Xp:6 to Xp:10. Seed 9 fell from Xp:11 to Xp:5. Seeds 4, 10, and 12 did not move. The mean fell by about 0.034. The brief patch did work. The operator ran for 1,695 seconds.

## What might solve it

On a tie, use the checkout. The checkout is the kept bot.

In `_keep_win`, show the two blocks and one order: copy the second block over the first, and change no other line. Remove the sentence "do not add 15". Do not name difficulty in the seed. A different condition on that line scored 0.081.

Leave `experience_level >= 12`, `_xp_farm_level`, the 20-square corpse cap, and the `MEASURE` patch.

## Result

- iteration 1: 0.081 not kept (no-cell-improved). Decreases the mean by 0.034 (from 0.114 to 0.081). Replaced the bonus test with monster difficulty. Seed 8 rose from 0.037 to 0.179. Seed 9 fell from 0.255 to 0.029.
