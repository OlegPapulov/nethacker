# Next experiment

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063). Raised several flee and Elbereth thresholds and ate more corpses from the pack.

## Why it stopped

died of starvation (1 of 15).

## What is the problem

Mean progress is 0.064. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

One game still starves. The parent already walks to a corpse once hunger is weak. Do not edit `eat_corpses_from_ground`. A distance cap there never runs, and eating sooner shortens the long games. Change only `imminent_death_on_melee` in `autoascend/combat/monster_utils.py`: raise the ordinary cut from 8 hit points to 10, and leave the dangerous-monster cut at 16. Do not edit Elbereth, melee priority, flee radii, or `eat_from_inventory`.

Edit `autoascend/` and exit. The judge measures that tree.
