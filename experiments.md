# Next experiment

## Result
- iteration 1: 0.0643 (no improvement over baseline 0.0643). Limited non-local corpse search to distance <= 3 when hunger is HUNGRY (< WEAK) to avoid wasting turns on long food hunts.

## Why it stopped
killed by a jackal (2 of 15).

## What is the problem
Mean progress is 0.0643 (unchanged). The bot still dies early on many seeds; avoiding long corpse-seeking trips when only mildly hungry saves turns but does not sufficiently improve survival.

## What might solve it
One coherent, general improvement is needed. Future work should focus on better early-game survival (combat/escape behavior) without exploiting seed-specific patterns.

Edit `autoascend/` and exit. The judge measures that tree.