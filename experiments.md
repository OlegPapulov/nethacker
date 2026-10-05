# Next mutator experiment

Applied. The score text no longer tells the operator to lengthen a short game. The one change is an assignment.

## Why it stopped

Run 37362877624 scored 0.04561779964972383. The parent is 0.11444300565928403. The mean falls by 0.069.

## What is the problem

The instructions say a longer short game raises the mean. The harness says the score rises when the bot descends. The operator then adds `descend_dry_floor`. Seed 9 falls from Xp:11 to Xp:7.

## What might solve it

Do not add a function. Do not add a stair. Leave the fainting latch unchanged. After that test, when `experience_level >= 11` and `level[1] > 2`, set `level = (Level.DUNGEONS_OF_DOOM, 2)`.

## Result

- iteration 1: 0.046 not kept (no-cell-improved). Decreases the mean by 0.069 (from 0.114 to 0.046). Seed 9 fell from 0.255 to 0.051.
