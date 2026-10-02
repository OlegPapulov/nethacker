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
