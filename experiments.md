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
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Drew a negative ring for a fast adjacent monster. The 15 seeds match the parent, because melee is still worth 16.
- iteration 1: 0.040 not kept (no-cell-improved). Decreases the mean by 0.037 (from 0.077 to 0.040). Visited unseen tiles before a search. Seeds 10 and 12 rose. Seed 13 fell from 0.179 to 0.024.
- iteration 1: 0.080 kept (registered). Increases the mean by 0.003 (from 0.077 to 0.080). Latched onto dungeon level 2 when fainting and no edible corpse was within 20 squares. The melee function did not change.
- iteration 1: 0.114 kept (registered). Increases the mean by 0.034 (from 0.080 to 0.114). Waited for experience level 12 before it left the first Doom level. Seeds 4, 8, 10, and 12 did not change. Seed 14 fell from 0.117 to 0.075.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Changed the launcher penalty. The 15 seeds match the parent.
- iteration 2: none. The job was cancelled at 360 minutes. No score.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Submitted the launcher edit again. The 15 seeds match the parent.
- next (proposal, not yet played): rewrite `current_strategy` (autoascend/global_logic.py). Let the food latch walk the farm target *past* dlvl 2 instead of latching on dlvl 2 forever.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is capped because every seed that survives the Doom farm stalls at experience level 9 (worth 0.117) and never reaches level 10 (worth 0.179). The wizard clears dungeon level 1, starves on the now-exhausted floor, and the food latch moves it one level down. The latch then stops: `_xp_farm_level` is set to 2 and never changes. If the wizard out-eats dlvl 2 as well, it starves there and dies with nothing new banked. The score is monotone (it keeps the highest experience depth ever seen), so any experience earned on floors 3, 4, ... before dying can only help a seed, never hurt it.

## What might solve it

Rewrite the one function `current_strategy` in `autoascend/global_logic.py`. Keep the existing trigger (hunger `FAINTING` with no edible corpse in reach) and the existing experience-level-12 stay, but when the wizard is already standing on its current farm floor and that floor's food is exhausted, move the farm target one level further down instead of latching permanently at dlvl 2. The target only ever increases (no oscillation), the wizard never leaves the Doom farm while merely weak, and the latch still fires only at fainting, so the score cannot drop for the seeds that already bank level 9. This is the change this tree carries.

Change the bot from the proposal above. The judge measures that tree.
