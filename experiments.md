# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37115352184 scored 0.077 against a 0.077 parent. The 15 seeds match the parent turn for turn. The tree is the spell-menu edit from the previous run, `a27b54a`.

## What is the problem

There is a code diff and no new bot. The spell parser does not change those 15 games. The note asked for a cast in `emergency_strategy`, and the operator submitted the parser again, with the cast deleted.

A fast monster that is already adjacent is ignored in `draw_monster_priority_negative`. The comment there says there is no point in running. Seeds 11 and 12 die to a bat on depth 1.

## What might solve it

The note names `draw_monster_priority_negative` and forbids `character.py` and the spell parser. When `imminent_death_on_melee` is true, a fast adjacent monster gets the same negative ring a slow one already gets. The `pass` does not stay. The 20-square corpse cap stays.

## Result

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Resubmitted the spell-menu tree. The 15 seeds match the parent.
