# Next mutator experiment

Applied with this change. The loop no longer plays the 15 seeds before the judge.

## Why it stopped

Run 37190939148 scored 0.114 against a 0.114 parent. The tree is the launcher edit from the cancelled run, `ba748d8`.

## What is the problem

The task says "Do not edit the `ret -= 6` line" and then "That launcher change scored 0.114." The number 0.114 is the parent score. The operator can read it as the score to reach. It then edits that line. The `ret += 15` line stays, so the 15 games do not move.

## What might solve it

Do not put 0.114 next to the launcher line. Say "Leave `ret -= 6` unchanged. A judged change to that line matched the parent on all 15 seeds." The only edit is the `ret += 15` line after `hitpoints > 8 or is_monster_faster`. When `blstats.depth` is 1 and the monster is not in `INSECTS`, that line does not add 15. Leave `experience_level >= 12`, `_xp_farm_level`, and the 20-square corpse cap.

## Result

- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Submitted the launcher edit again. The 15 seeds match the parent.

## Result

- iteration 1: 0.114 not kept (no-cell-improved).

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

no finished games (0 of 0).

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Leave `_xp_farm_level` in place. Do not edit it. Leave `experience_level >= 12` in place. Do not raise it. Do not edit `global_logic.py` or `exploration_logic.py`. Leave `ret -= 6` unchanged. A judged change to that line matched the parent on all 15 seeds. Seeds 4, 8, 10, and 12 die under 10,000 turns. In `melee_monster_priority`, the line is `ret += 15` after `hitpoints > 8 or is_monster_faster`. When `blstats.depth` is 1 and the monster is not in `INSECTS`, do not add 15. A soldier ant keeps the bonus. Edit only that line.

Edit only the function named above. The judge measures that tree.

