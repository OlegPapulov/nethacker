# Next mutator experiment

Applied. The instruction engraves Elbereth only when no monster is adjacent.

## Why it stopped

Run 37310611617 scored 0.11101507289173372. The parent is 0.11444300565928403. The mean falls by 0.003.

## What is the problem

The operator engraved Elbereth in `emergency_strategy` and left the rest loop commented. Seed 4 rose from 0.018 to 0.117. Seed 3 fell from 0.179 to 0.029. The long game got shorter, so the mean fell.

The operator did not copy the depth test. The code uses `depth <= 3` and skips undead, demons, and mindless monsters. Seed 3 died at depth 1.

## What might solve it

Do not tell the operator to engrave while a monster is adjacent. `emergency_strategy` runs before `fight2`. Prayer and a healing potion run first. When those do not fire, the write takes the turn, and the monster attacks before the word is on the floor.

The instruction now says: in `emergency_strategy`, engrave Elbereth once when `blstats.depth` is 1, hit points are below 6, `can_engrave()` is true, and no monster is adjacent. Do not call `direction('.')`. Do not remove the comment marks on the rest loop. The file that may change is `agent.py`.

That write can still fail to run. Hit points usually fall while a monster is already adjacent, so the safe test may never be true. A tree that matches the parent is thrown away.

Leave `fight_heur.py` forbidden. Leave the level-12 gate, the food latch, and the corpse cap.

## Result

- iteration 1: 0.111 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.114 to 0.111). Seed 4 rose from 0.018 to 0.117. Seed 3 fell from 0.179 to 0.029.
