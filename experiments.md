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
