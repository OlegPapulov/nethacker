# Next mutator experiment

Applied. The edit is one test on the fainting latch. Combat functions stay closed.

## Why it stopped

Run 37349624888 scored 0.09228385325013148. The parent is 0.11444300565928403. The mean falls by 0.022.

## What is the problem

The operator edited `fight2`. The tie-break left seed 4 at 2,742 turns and lowered seed 9 from Xp:11 to Xp:10. Earlier edits in `emergency_strategy` did the same kind of harm.

The kept gains are the corpse cap, the fainting latch, and the level-12 gate. Those edits are in `global_logic.py`. Seeds 4, 10, and 12 die at Xp:2, Xp:4, and Xp:5, on depth 2. The latch can send a fainting wizard downstairs before level 5.

## What might solve it

In `current_strategy`, the fainting test that sets `_xp_farm_level` to 2 also requires `experience_level >= 5`. Do not change `experience_level >= 12`. Do not edit `fight2` or `emergency_strategy`.

## Result

- iteration 1: 0.092 not kept (no-cell-improved). Decreases the mean by 0.022 (from 0.114 to 0.092). Seed 4 stayed at 2,742 turns. Seed 9 fell from 0.255 to 0.179.

## Result

- iteration 1: 0.102 not kept (no-cell-improved).

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
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Drew a negative ring for a fast adjacent monster. The 15 seeds match the parent, because melee is still worth 16.
- iteration 1: 0.040 not kept (no-cell-improved). Decreases the mean by 0.037 (from 0.077 to 0.040). Visited unseen tiles before a search. Seeds 10 and 12 rose. Seed 13 fell from 0.179 to 0.024.
- iteration 1: 0.080 kept (registered). Increases the mean by 0.003 (from 0.077 to 0.080). Latched onto dungeon level 2 when fainting and no edible corpse was within 20 squares. The melee function did not change.
- iteration 1: 0.114 kept (registered). Increases the mean by 0.034 (from 0.080 to 0.114). Waited for experience level 12 before it left the first Doom level. Seeds 4, 8, 10, and 12 did not change. Seed 14 fell from 0.117 to 0.075.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Changed the launcher penalty. The 15 seeds match the parent.
- iteration 2: none. The job was cancelled at 360 minutes. No score.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Submitted the launcher edit again. The 15 seeds match the parent.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The score is the mean of the 15 judge seeds. A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Leave `experience_level >= 12` in place. Do not raise it. Do not edit `fight_heur.py`, `fight2`, `emergency_strategy`, or `exploration_logic.py`. Seed 4 dies at 2,742 turns and stops at Xp:2. Seeds 10 and 12 die under 10,000 turns and stop at Xp:4 and Xp:5. Seed 3 is at Xp:10. Seed 9 is at Xp:11. Those games must keep that progress. Do not edit `emergency_strategy`. Do not add `search`, `move`, `engrave`, or a loop there. Do not edit `fight2`. A melee tie-break there left seed 4 at 2,742 turns and lowered seed 9 from Xp:11 to Xp:10. The function you may change is `current_strategy` in `global_logic.py`. On the fainting test that sets `_xp_farm_level` to 2, also require `experience_level >= 5`. A wizard at Xp:2 must stay on dungeon level 1. Do not add an engrave. Do not remove the comment marks on the Elbereth block. The file you may change is `global_logic.py`. Every other file matches the parent.

Edit only the function named above. The judge measures that tree.

