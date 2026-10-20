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

## Proposal

Rewrite `imminent_death_on_melee` in `autoascend/combat/monster_utils.py`. The non-dangerous-monster flee line sits at 8 hit points: the wizard trades blows with a jackal or goblin until one hit from death before the flee ring kicks in, and by then it is often too late. Raise that line to 12. The dangerous-monster line at 16 is measured and untouched. The lower list names "Dropping the melee bonus for a faster monster" — that is the +15 engagement bonus, not the flee ring. The leave list names "Raising the dangerous-monster melee line from 16 to 20" — that is the other line. The non-dangerous line at 8 appears in no list. A nearby number on the dangerous line is the same action; a change to the non-dangerous line is not.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. You do not know that mean until the judge plays the 15 seeds. Your task is to raise the score. You use the knowledge in `GAME_RULES.md`. The lists there name the actions that raise the score, the actions that lower the score, and the actions that leave the score where it is. Make one change. That change is one new function, or one rewrite of one function. Do not repeat a listed action. A listed action is a finished measurement. A listed action covers the measured situation and a similar situation. A similar situation is the same action. Do not rewrite a listed action. When the change you can name is a listed action, leave the bot as it is. Do not revert the change. The judge scores the tree you exit with. An older mean in this file is not the current parent. The ends in `experience.md` are not the proposal. Propose one change in this file, in accordance with the game rules. Name the one function you add or the one function you rewrite. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
