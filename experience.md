# Playthrough

Identity: `wiz-hum-cha-mal`

## Games

15 seeds, mean progress 0.1144. The wizard farms XP on Doom levels 1-2 until experience level 12, then explores deeper.

| Seed | Xp | Depth | Turns | Progress | Death |
|------|-----|-------|-------|----------|-------|
| 0 | 9 | 1 | 50145 | 0.117 | poisoned by an orcish arrow |
| 1 | 10 | 1 | 46006 | 0.179 | killed by a killer bee |
| 2 | 8 | 1 | 34154 | 0.075 | killed by a bolt of fire |
| 3 | 10 | 3 | 57042 | 0.179 | poisoned by an orcish arrow |
| 4 | 2 | 2 | 2742 | 0.018 | killed by a goblin |
| 5 | 10 | 1 | 55705 | 0.179 | killed by a giant bat |
| 6 | 10 | 3 | 73840 | 0.179 | killed by a plains centaur |
| 7 | 9 | 6 | 34611 | 0.117 | killed by a vampire bat |
| 8 | 6 | 1 | 9957 | 0.037 | killed by a newt |
| 9 | 11 | 3 | 69906 | 0.255 | killed by an invisible Mordor orc |
| 10 | 4 | 2 | 6313 | 0.024 | killed by a kitten |
| 11 | 8 | 4 | 23577 | 0.075 | killed by a pony |
| 12 | 5 | 2 | 5011 | 0.029 | killed by a kobold lord |
| 13 | 10 | 5 | 48694 | 0.179 | killed by a dwarf lord |
| 14 | 8 | 1 | 32018 | 0.075 | killed by a bolt of cold |

## Why it stopped

Six seeds reach Xp:10-11 (progress 0.179-0.255). Two seeds reach Xp:9 (progress 0.117). Seven seeds die early at Xp:2-8 (progress 0.018-0.075), dragging the mean down.

The early deaths are the problem. Seeds 4, 8, 10, and 12 die at Xp:2-6 with only 2742-9957 turns. These deaths are to weak monsters: goblin, newt, kitten, kobold lord. The wizard is fragile and dies to melee combat when it should not.

Seeds 2, 11, and 14 die at Xp:8 to ranged attacks (bolt of fire, pony, bolt of cold). The wizard has no ranged attack of its own and cannot fight back against ranged monsters.

## What is the problem

The wizard starves or weakens before it can farm enough XP. When hunger rises, the wizard spends turns walking to food instead of gaining XP. By the time it finds food, it is already weak and easy prey for the first monster that arrives.

The current food logic allows the wizard to walk up to 5 squares for food when hungry, and up to 20 squares when weak. But the wizard often gets weak before it finds food, because 5 squares is not far enough when corpses are scattered across the level.

## What might solve it

Allow the wizard to walk up to 20 squares for food when hungry, not just when weak. This would help it find food earlier, avoid getting weak, and survive long enough to farm XP. See `experiments.md`.
