# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37123137695 scored 0.077 against a 0.077 parent. Progress and turn count match the parent on every seed.

## What is the problem

The operator did edit `draw_monster_priority_negative`. A fast adjacent monster now gets a negative ring. `fight2` still picks melee, because `melee_monster_priority` adds 15 for any faster monster, even at 1 hit point. That swing is worth 16. A step off the ring is worth less, so the 15 games do not move. The same tree also resubmits the spell parser.

## What might solve it

The note names the five games under 10,000 turns: a kobold zombie, two bats, a coyote, and a newt, all on depth 1. A soldier ant that already lasts about 20,000 turns is not the edit. In `melee_monster_priority`, do not add 15 when `imminent_death_on_melee` is true, including for a monster that is not faster. The swing ranks below a step onto an adjacent walkable square. The 20-square corpse cap stays.

## Result

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Drew a negative ring for a fast adjacent monster. The 15 seeds match the parent, because melee is still worth 16.
