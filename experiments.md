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

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Change one test that already exists. Do not add a new action. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

## Proposed change (iteration: parent + 1)

The parent is 0.114. Two seeds die to monsters the wizard cannot fight back
against, because the wizard itself is the only thing that can make them
hostile: tid 10 "killed by a kitten" (Xp:4) and tid 11 "killed by a pony"
(Xp:8). A pet or a peaceful monster is never targeted by melee or ranged
(`get_visible_monsters` excludes `G.PETS` and `peaceful_monster_mask`), so the
only way the wizard hits one is a wand ray. In `_simulate_wand_path`
(combat/fight_heur.py:140), a pet on the beam is collateral worth `-20*p`, but a
peaceful monster falls through to `monster = None` and costs nothing, although
the beam still hits it and turns it hostile. The launcher already refuses such
shots (`ranged_priority` returns `None` for a monster with no visible target);
the wand path is missing the same check.

Change one existing test: the `elif inside(agent, y, x) and
agent.glyphs[y, x] in G.PETS:` branch in `_simulate_wand_path` also treats a
monster on `agent.monster_tracker.peaceful_monster_mask[y, x]` as
collateral, so a peaceable creature in the beam costs the same `-20*p` as a
pet. No new action; no other test touched. Either the affected seeds (10, 11)
stop dying to monsters they start themselves and bank a higher Xp, or the mean
stays at 0.114.

Change the bot from the proposal above. The judge measures that tree.
