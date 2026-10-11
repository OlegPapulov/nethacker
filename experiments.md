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

## Result

- iteration 1: submitted, awaiting judge. Rewrote `fight2` in `autoascend/agent.py` (one function rewrite). Locally (arbitrary seeds, `make_environment` + `TrajectorySpec`, same four seeds run before and after): no seed regressed (the unchanged seeds are turn-for-turn identical to the parent), and seed 1010 went from Xp:5 (0.0291) to Xp:7 (0.0508) by breaking a starvation lock.

## Last iteration

Rewrite of one function: `Agent.fight2` in `autoascend/agent.py`.

The bot lost because corpses in the mapped dlvl-1 interior stopped being eaten once the wizard was inside a fight. Traces of the starvation deaths show the wizard on Elbereth for 40+ turns at HP 15-21 waiting out a sewer rat while hunger dropped from WEAK to FAINTING, then walking for the down staircase at FAINTING with the bat that killed it; in both stages the corpse register shows an edible corpse inside the normal 20-square corpse-search reach (the non-rotting lichens at distance 0-6) that was never touched. No strategy could interrupt that: the parallel `eat_corpses_from_ground` WEAK preempt cannot fire while `fight2` already owns the iteration loop, so the food the wizard could already reach went uneaten and the score-raising food latch only closes at FAINTING, too late and onto a lethal walk.

The rewrite does not change the corpse-search reach (20), the freshness window (50), the fainting latch, force bolt gating, prayer, or the faster-monster melee bonus. Inside `fight2`, when hunger is at least WEAK, a passive best action (wait/search, or walking while FAINTING) is replaced by closing the existing corpse-search reach on the nearest edible corpse and eating it: exactly the same filters and reach `eat_corpses_from_ground` uses, just reachable when a fight already holds the loop. Melee/ranged/zap actions are never overridden, so active fights are untouched (the Xp:10 farm seeds reproduce the parent turn for turn).

## Why it stopped

The parent batch is not in this note. The earlier "previous tree scored 0.138" warning describes a different diff; the proposal above is a new one.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Your task is to raise the score. You use the knowledge in `GAME_RULES.md`. Make one change. That change is one new function, or one rewrite of one function. Do not repeat a listed action. The one change raises the score. It does not lower the score. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. `experience.md` holds the ends of the played games. Read it and describe why the bot lost. Propose one change in this file, in accordance with the game rules. Name the one function you add or the one function you rewrite. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
