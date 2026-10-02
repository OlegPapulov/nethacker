# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36934535247 scored 0.063 and 0.060 against a 0.064 parent. Neither was kept.

## What is the problem

Both edits made the wizard walk to food sooner. The parent already does that at weak hunger. Earlier eating spends the turns that produce the deep games, so the mean falls. The loop also started from whatever was on `main`, not from the best public commit for the identity being played.

## What might solve it

Before evolve, for the identity in this run, pull this owner's public program with the highest progression and use it as the seed. If that identity has no public row, pull `8387c34`, the AutoAscend import. The note written for the agent says to leave the weak-hunger threshold alone.

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.

## Result

- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064).
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063).

## Proposal (not approved)
Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.

# Next experiment

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.

## Why it stopped

killed by a jackal (2 of 15).

## What is the problem

Mean progress is 0.064. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

One game still starves, and the parent already walks to a corpse once hunger is weak. Eating any sooner spends the turns the deep games used to descend, and the mean falls. Leave that threshold. Change one other decision in autoascend.

Edit `autoascend/` and exit. The judge measures that tree.

