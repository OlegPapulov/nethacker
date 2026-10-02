# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36983992379 scored 0.064 and 0.064 against a 0.064 parent. Neither was kept. Both judged trees match the parent on every seed.

## What is the problem

The operator spent 154 and 178 minutes and did not leave a Python change. Iteration 2 wrote a notebook into `experiments.md` claiming several local measurements, then restored the parent. The judge scored that parent. The 8-to-10 hit-point cut was never in the tree the judge ran.

The operator brief says to measure a sample and that a matching score is discarded. The seed note asked for a one-point threshold change and said not to run the arena. The model followed the brief and reverted.

`parse_spellcast_view` returns immediately unless the role is a healer. A wizard's spell list stays empty, and the healing casts in `emergency_strategy` are commented out.

## What might solve it

The note says to leave the edit in the files. Restoring the parent is a wasted iteration. The edit parses the spell menu for a wizard and casts `force bolt` when it is known, energy is at least 5, and a monster is adjacent. Hunger, search, and hit-point cuts stay as they are.

## Result

- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The tree matches the seed.
- iteration 2: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The agent wrote a notebook and left the parent in place.

## Result

- iteration 1: 0.077 kept (registered). Increases the mean by 0.013 (from 0.064 to 0.077).
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077).

## Proposal (not approved)
Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.

# Next experiment

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063). Raised several flee and Elbereth thresholds and ate more corpses from the pack.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The tree matches the seed.
- iteration 2: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The agent wrote a notebook and left the parent in place.

## Why it stopped

died of starvation (1 of 15).

## What is the problem

Mean progress is 0.064. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

One game still starves. Do not edit hunger, search, or hit-point cuts, and do not edit `eat_corpses_from_ground`. `parse_spellcast_view` returns immediately unless the role is a healer, so a wizard's spell list stays empty and `cast` never runs. Parse that menu for a wizard the same way as for a healer. In `emergency_strategy`, when `force bolt` is known, energy is at least 5, and a monster is adjacent, cast it. Leave both edits in the tree. Do not revert them after a local game.

Edit `autoascend/` and exit. The judge measures that tree.

