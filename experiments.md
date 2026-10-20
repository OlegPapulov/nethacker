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

## Last iteration

The previous tree scored 0.148 and was not kept. Do not submit that same diff again.

## This iteration

Proposal: no code change. Name no new function and rewrite no function. Leave the
bot as it is. The tree exits matched to the parent.

Reason. I reproduced the parent on seed 1 with an in-process oracle (no arena
run): 0.2548, Xp:11, depth 1, killed by a dwarf lord near turn 66905, identical
to `/refs/parent-eval.json`. I then checked every change I could name against
`GAME_RULES.md`. All five raise actions are already present in the tree: the
experience-level-12 farm gate; skill points into the wielded weapon
(`select_skill_to_upgrade` returns `main_hand.sub`); the force-bolt cast at
2-8 squares from experience level 10 with the 20,000-turn re-read; the
floating-eye refusal when another monster is within 2 squares; and the
six-trap block in the 50-turn window. Every other change I could name is a
listed lower action (force bolt timing/distance, early food latch, earlier
hunger prayer, dangerous-set for a dwarf/rothe/orc, melee lines at 8/16,
healing/speed potion thresholds, Elbereth at HP<30, metal-suit swap, ring wear)
or a listed neutral action (corpse caps, fainting search reach, trap-window
subset, faster-monster bonus, Elbereth while a faster monster approaches,
sickness prayer/eat, error catch, 150-step guard). The rules say a listed action
covers a similar situation and that when the change I can name is a listed
action I must leave the bot as it is.

I also tested three changes, and all three confirm the tree is a tuned local
optimum on this axis set:
- Skip the auto-SPACE in `update` while the wizard is engulfed: much worse
  (seed 1 fell to 0.1170 at Xp:9, stalled spamming ESC on the fog-cloud message).
- Drop `parse_enhance_view` from `fight2` while blind/confused/stunned: no
  effect (bit-identical to the parent on seed 1).
- Read the enhance menu only once per experience level: worse. Seed 1 fell from
  0.2548 to 0.1791 (Xp:11 to Xp:10), because the mid-fight menu read is what
  spends the level's skill points before the next fight.

The fatal pattern on seed 1 is a dust-vortex engulf landing while the wizard is
fainting from lack of food, then a dwarf lord hit; the fainting is the food
latch, which the rules pin to the fainting-and-no-edible-corpse test. I found no
unlisted, non-stalling change to name. The tree exits unchanged.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. You do not know that mean until the judge plays the 15 seeds. Your task is to raise the score. You use the knowledge in `GAME_RULES.md`. The lists there name the actions that raise the score, the actions that lower the score, and the actions that leave the score where it is. Make one change. That change is one new function, or one rewrite of one function. Do not repeat a listed action. A listed action is a finished measurement. A listed action covers the measured situation and a similar situation. A similar situation is the same action. Do not rewrite a listed action. When the change you can name is a listed action, leave the bot as it is. Do not revert the change. The judge scores the tree you exit with. An older mean in this file is not the current parent. The ends in `experience.md` are not the proposal. Propose one change in this file, in accordance with the game rules. Name the one function you add or the one function you rewrite. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
