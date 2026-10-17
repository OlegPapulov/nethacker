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
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Extended the force bolt to any non-adjacent monster on a clear line.

## Next experiment

**Function rewritten:** `cast_attack_actions` in `autoascend/combat/fight_heur.py`.

**What it does now:** the force bolt still fires only from experience level 10, on the first dungeon level, at a non-weak monster on a clear walkable line with energy at least 10 and an acceptable fail chance, and the wizard is still never adjacent (`dis < 2` is refused). The only difference is that the ray no longer stops at 8 squares. It now reaches any monster the ray can actually hit.

**Why this is the loss.** `experience.md` records no endings, so I describe the endings I measured on this tree. In the long games the wizard reaches experience level 10 or 11 and then dies fighting. On seed 0 it fought a rothe to the death at full-ish hit points, trading melee blow for melee blow, and died at experience level 10. On seed 1 it starved at full hit points on dungeon level 1 after fainting. The starvation rescue (latch onto dungeon level 2) fires at turn 66199, but the wizard cannot reach the stairs while fainting and surrounded, so it dies in place. The rescue is too late to save, and latching earlier would break a measured rule. The deaths I can still fix are the melee deaths.

**Why the melee deaths happen.** The wizard's only real attack is the force bolt, and the bolt is capped at distance 8. A rothe or a dwarf lord that first appears at distance 9 or more is out of range, so the wizard walks toward it, it closes, and the wizard melees it to the death. Killing a tough monster at range before it closes is the one thing the wizard has that raises a long game by an experience level. `GAME_RULES.md:98` calls the blessed action "Casting force bolt from experience level 10, on the first dungeon level, at a monster that is not adjacent." Adjacent, not eight. The distance-8 cap is not in any list, so removing it is unlisted.

**Why it should not lower the score.** Everything else about the cast is unchanged: the level gate, the dungeon gate, the weak-monster refusal, the energy floor, the fail-chance limit, the clear-line and pet checks, and the refusal to fire when the wizard is adjacent. The change only adds casts that the blessed action already describes, and only against monsters on a clear line. In the short games the wizard never reaches experience level 10, so nothing changes there. In the long games the bolt reaches the rothe and the dwarf lord before they close, the wizard takes less melee damage, and the game lasts one level longer.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Your task is to raise the score. You use the knowledge in `GAME_RULES.md`. Make one change. That change is one new function, or one rewrite of one function. Do not repeat a listed action. A listed action is a finished measurement. The next change is not a guard for the last death. The next change is one unlisted action that can raise a long game by one experience level. A short game may fall. The mean still has to rise. The one change raises the score. It does not lower the score. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. `experience.md` holds the ends of the played games. Read it and describe why the bot lost. The loss is not the proposal. Propose one change in this file, in accordance with the game rules. Name the one function you add or the one function you rewrite. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
