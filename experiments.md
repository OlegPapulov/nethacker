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
