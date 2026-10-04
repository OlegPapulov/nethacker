# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37159253981 scored 0.114 against a 0.080 parent. The child was kept. The operator changed the experience-level gate from 8 to 12. The operator did not edit `melee_monster_priority`.

## What is the problem

The gate helps games that already reach experience level 8. Seeds 4, 8, 10, and 12 die earlier. Their turn counts did not change, so this gate cannot raise them. Seed 14 fell from 0.117 to 0.075, so a higher gate is not free. The depth-1 melee bonus is still in the file.

## What might solve it

Leave `experience_level >= 12` in place. Do not raise it. Leave `_xp_farm_level` and the 20-square corpse cap in place. In `melee_monster_priority`, do not add 15 when `blstats.depth` is 1 and the monster is not in `INSECTS`. Every other file matches the parent. The operator writes the `# hypothesis:` comment and the line in `experiments.md` in ASD-STE100 style.

## Result

- iteration 1: 0.114 kept (registered). Increases the mean by 0.034 (from 0.080 to 0.114). Waited for experience level 12 before it left the first Doom level. Seeds 4, 8, 10, and 12 did not change. Seed 14 fell from 0.117 to 0.075.
