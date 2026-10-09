# Next experiment

## Fight from a chokepoint

The wizard loses the long games by standing in an open room where two or three
monsters reach it every turn (seeds 3, 9, 13), and it loses the hurt games
because it keeps giving ground in the open instead of behind a wall. The first
tip says a doorway or a corridor lets only one monster hit while an open room
lets several. The parent built a corridor priority map for exactly this and left
it commented out (`get_corridors_priority_map` in `combat/fight_heur.py`).

Add one behaviour: while the wizard is in a fight and is either hurt (hit points
at or below 8, the same threshold the melee bonus already cares about) or
outnumbered (two or more non-weak monsters adjacent), it prefers to move onto a
doorway or corridor tile -- a walkable tile with six or more blocked neighbours
of the eight, which is what a one-tile-wide passage or a door in a wall is. The
tiles get a movement weight just above the melee weight, so a healthy wizard
still trades blows against one monster, but a hurt or surrounded wizard steps
into the passage and then fights from it (once standing on the chokepoint its
own bonus cancels out relative to the current square, so it stops moving and
attacks).

Two gates keep this away from the measured tests and the fast-monster code: it
never fires when a faster monster is adjacent (the `+15` melee rule still decides
that), and it never fires outside a fight or with only one adjacent monster at
full hit points. Weak monsters do not count as the crowd.

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

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Leave every listed test as it is, including a nearby number in the same function. Do not change a number in an existing test. Add one behavior the listed tests do not already cover. That behavior raises the experience level a game reaches. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
