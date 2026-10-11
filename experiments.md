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
- iteration 1: 0.138 not kept (no-cell-improved). Does not change the mean (0.138). Rewrote `keep_attack_spell_memorized` to re-read the force-bolt book when it becomes due. The 15 seeds match the parent, because the farm floor is permanently crowded on the top seeds, and the re-read defers forever while a monster is within 5.

## Last iteration

The previous tree scored 0.138 and was not kept. Do not submit that same diff again.

## Why it stopped

The parent evaluation played all 15 seeds and all 15 games die. Seven reach Xp10-11, and five of those still die in melee after 50k-92k turns on the crowded farm floor (ants, orc, hobbit, dwarf lords) where force bolt is the only escape. Details per seed are in `experience.md`.

## What is the problem

The spell re-read works but its deferral never completes on the crowded seed floors: the strategy waits for a moment with no monster within 5, and those floors always have one, so the read is starved forever and the Xp11 games die in melee at the farm exit.

## What might solve it

The judge score is the mean of 15 seeds; a child is kept only when that mean is strictly higher. The one change is a rewrite of one function, `keep_attack_spell_memorized`. It cannot wait forever for a quiet farm floor, because on the seed-crowded floors a quiet moment may never come. Extend the parent deferral with an escalation: keep waiting while the read is barely due or a monster is adjacent, but once the spell has been due for 5000 extra turns since the last successful read (`blstats.time - _last_spell_read_turn['force bolt'] >= 25000`) and no monster is within 2, read the book anyway, accepting the mid-study interrupt risk. The remaining logic (find the dropped book on the level, take it, read it, drop it again) is untouched, and uncrowded games defer exactly like the parent until the deadline passes, so their turns are unchanged.

Change the bot from the proposal above. The judge measures that tree.
