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

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Replaced the `pass` for a fast adjacent monster with the negative ring that is already drawn for a fast monster that is not adjacent yet (-5 at radius 1, -10 at radius 2). Measured all 15 seeds: identical to the parent, because a melee action is worth 16 (`fight_heur.melee_monster_priority`) and a negative ring cannot beat it. Also measured and rejected: the literal slow-monster ring (-10 at radius 1) 0.066, a retreat attractor at +17 over radius 2 for every fast adjacent monster 0.032-0.057, a fainting-only retreat 0.0615, and a flee-from-flyers attractor, which survived two bat deaths but never gained XP and burned 10x the steps.

## Why it stopped

killed by a soldier ant (2 of 15).

## What is the problem

Mean progress is 0.077. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The usual stop is killed by a soldier ant. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Do not edit `character.py` or the spell parser. That tree was scored: all 15 seeds match the parent, and the smoke seed is 1,899 turns. In `draw_monster_priority_negative`, a fast monster that is already adjacent is ignored (`pass`). That is the bot standing in the melee. When `imminent_death_on_melee` is true, draw the same negative ring for a fast adjacent monster that you already draw for a slow one. Do not leave the `pass`. Edit only that function.

Edit `autoascend/` and exit. The judge measures that tree.
