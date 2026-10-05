# Next mutator experiment

Applied. The instruction no longer asks for an Elbereth write. Seed 4 must last longer, and seed 3 and seed 9 must keep their progress.

## Why it stopped

Run 37331933484 scored 0.10213461846666004. The parent is 0.11444300565928403. The mean falls by 0.012.

## What is the problem

The operator followed the safe test. The write runs when depth is 1, hit points are below 6, and no monster is adjacent. The rest loop stays commented.

Seed 4 rose from Xp:2 to Xp:7. Seed 8 rose from Xp:6 to Xp:8. Seed 3 fell from Xp:10 to Xp:5. Seed 13 fell from Xp:10 to Xp:8. The losses are larger than the gains.

The word changes the next fight. `wait_action` returns about 30 when the floor says Elbereth. Melee, ranged, and zap each lose 100. The bot stands on the word and stops the attacks that used to raise the long games.

## What might solve it

The culprit is the wait after the word is written. `wait_action` then outranks melee in every game that reaches that square. Seed 4 and seed 3 share that code.

The shortest parent game is seed 4, at 2,742 turns and Xp:2. A longer seed 4 raises the mean only when the long games keep their progress. The last two writes lengthened seed 4 and shortened seed 3. Seeds 10 and 12 stayed at Xp:4 and Xp:5.

Do not tell the operator to edit only for the shortest run. The judge still scores all 15 seeds, and the edit is one function. Do not send another Elbereth write.

Leave `fight_heur.py` forbidden. Leave the level-12 gate, the food latch, and the corpse cap. Leave the commented rest loop in place.

## Result

- iteration 1: 0.102 not kept (no-cell-improved). Decreases the mean by 0.012 (from 0.114 to 0.102). Seed 4 rose from 0.018 to 0.051. Seed 8 rose from 0.037 to 0.075. Seed 3 fell from 0.179 to 0.029. Seed 13 fell from 0.179 to 0.075.

## Result

- iteration 1: 0.084 not kept (no-cell-improved).
- iteration 2: 0.074 not kept (no-cell-improved). Decreases the mean by 0.009 (from 0.084 to 0.074).

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

## Last iteration

The previous tree scored 0.084 and was not kept. Do not submit that same diff again.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The score is the mean of the 15 judge seeds. A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Leave `_xp_farm_level` in place. Do not edit it. Leave `experience_level >= 12` in place. Do not raise it. Do not edit `fight_heur.py`, `global_logic.py`, or `exploration_logic.py`. Seed 4 dies at 2,742 turns and stops at Xp:2. Seeds 10 and 12 die under 10,000 turns and stop at Xp:4 and Xp:5. Seed 3 is at Xp:10. Seed 9 is at Xp:11. Those games must keep that progress. Do not add an engrave in `emergency_strategy`. Do not remove the comment marks on the Elbereth block. That block rests for 8 turns. When the floor says Elbereth, the bot waits, and a long game gets shorter. Do not call `direction('.')`. The file you may change is `agent.py`. Every other file matches the parent.

Edit only the function named above. The judge measures that tree.

