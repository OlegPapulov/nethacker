# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37115352184 scored 0.077 against a 0.077 parent. The 15 seeds match the parent turn for turn. The tree is the spell-menu edit from the previous run, `a27b54a`.

## What is the problem

There is a code diff and no new bot. The spell parser does not change those 15 games. The note asked for a cast in `emergency_strategy`, and the operator submitted the parser again, with the cast deleted.

A fast monster that is already adjacent is ignored in `draw_monster_priority_negative`. The comment there says there is no point in running. Seeds 11 and 12 die to a bat on depth 1.

## What might solve it

The note names `draw_monster_priority_negative` and forbids `character.py` and the spell parser. When `imminent_death_on_melee` is true, a fast adjacent monster gets the same negative ring a slow one already gets. The `pass` does not stay. The 20-square corpse cap stays.

## Result

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Resubmitted the spell-menu tree. The 15 seeds match the parent.

## Result

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077).

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
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). No code change.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Read the spell menu and deleted the cast.
- iteration 1: none not kept (gate:child identical to parent). The tree matched the parent, so the judge did not run.
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Resubmitted the spell-menu tree. The 15 seeds match the parent.

## Why it stopped

killed by a soldier ant (2 of 15).

## What is the problem

Mean progress is 0.077. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The usual stop is killed by a soldier ant. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Do not edit `character.py` or the spell parser. That tree was scored: all 15 seeds match the parent, and the smoke seed is 1,899 turns. In `draw_monster_priority_negative`, a fast monster that is already adjacent is ignored (`pass`). That is the bot standing in the melee. When `imminent_death_on_melee` is true, draw the same negative ring for a fast adjacent monster that you already draw for a slow one. Do not leave the `pass`. Edit only that function.

Edit `autoascend/` and exit. The judge measures that tree.

