# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37023219996 kept iteration 1 at 0.077 against a 0.064 parent. Iteration 2 scored the same 0.077 and was not kept. The record commit did not contain the bot.

## What is the problem

The loop copied the kept tree into the pulled parent directory. The record step commits the checkout, so `main` stayed on the 0.064 bot.

The score moved because a weak-hunger corpse walk now stops at 20 squares. The force bolt block does not run: `parse_spellcast_view` is never called, and `_parse` clears `known_spells`.

## What might solve it

Write a kept tree onto the checkout. The next note leaves the 20-square cap alone. It tells the agent to call `parse_spellcast_view` once the role is known, and to stop clearing `known_spells` inside `_parse`. Do not hardcode a spell letter.

## Result

- iteration 1: 0.077 kept (registered). Increases the mean by 0.013 (from 0.064 to 0.077). Capped a weak-hunger corpse walk at 20 squares.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). The judge table matches iteration 1.

## Result

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077).
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
- iteration 1: 0.077 kept (registered). Increases the mean by 0.013 (from 0.064 to 0.077). Capped a weak-hunger corpse walk at 20 squares.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). The judge table matches iteration 1.

## Why it stopped

killed by a soldier ant (2 of 15).

## What is the problem

Mean progress is 0.077. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The usual stop is killed by a soldier ant. Leave the weak-hunger corpse walk capped at 20 squares. That cap raised the mean from 0.064 to 0.077. Do not edit it. `parse_spellcast_view` is never called, and `_parse` sets `known_spells` to an empty dict, so the force bolt block does not run. Call `parse_spellcast_view` once the role is known, and stop clearing `known_spells` inside `_parse`. Do not hardcode a spell letter. Leave that edit in the tree. Do not revert it.

Edit `autoascend/` and exit. The judge measures that tree.

