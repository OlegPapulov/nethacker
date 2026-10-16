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

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Your task is to raise the score. You use the knowledge in `GAME_RULES.md`. Make one change. That change is one new function, or one rewrite of one function. Do not repeat a listed action. A listed action is a finished measurement. The next change is not a guard for the last death. The next change is one unlisted action that can raise a long game by one experience level. A short game may fall. The mean still has to rise. The one change raises the score. It does not lower the score. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. `experience.md` holds the ends of the played games. Read it and describe why the bot lost. The loss is not the proposal. Propose one change in this file, in accordance with the game rules. Name the one function you add or the one function you rewrite. Change the bot from that proposal.

## The one change

Add one function: `chokepoint_fight_priority(agent, priority, walkable, monsters)` in `combat/fight_heur.py`, called once from `get_priorities`.

### Why this one

The long games die in melee on the first Doom floors: nine of the fifteen ends
are a single strong monster (rothe, dwarf lord, fire ant, soldier ant, Mordor orc,
pony) that closes on the wizard while it stands in an open room, where every
monster that can reach it hits it in the same turn. `GAME_RULES.md` states the
counter plainly: "A fight in a doorway lets one monster hit. A fight in a corridor
lets one monster hit. An open room lets several monsters hit." That tip is not on
any score list, so using it is not repeating a listed action. The parent already
ships `get_corridors_priority_map`, but never calls it, so the wizard never seeks
the chokepoint the tip describes.

The one function biases the movement heatmap toward nearby doorway/corridor
tiles *only* while the wizard is facing a group of two or more real threats that
are not yet adjacent, and never while it is already standing in a chokepoint.
It is a movement nudge during the approach, before the tuned melee action takes
over, so it does not touch `melee_monster_priority` (melee is still worth 16),
does not lower the melee bonus for a faster monster, does not start a fight
beyond the current reach, and does not step toward a doorway because the wizard
is hurt or because two monsters are adjacent -- every one of those is a listed
action and none of them is the trigger here. When only one monster is present or
the monsters are already adjacent the function returns without changing
anything, so the parent's behaviour is preserved in exactly the games it already
wins.

### What it should do

Funnelling a group through one doorway lets the wizard trade one blow per turn
instead of several, which is the difference between winning the fight and dying
at experience level 10 or 11. Surviving one more of those fights is one more
experience level on a long game, which is what raises the mean.

Change the bot from the proposal above. The judge measures that tree.
