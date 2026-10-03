# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37077364014 scored 0.077 and 0.077 against a 0.077 parent. Neither was kept. The 15 judge seeds match the parent turn for turn.

## What is the problem

Iteration 1 changed no Python. Iteration 2 read the spell menu and then deleted the cast. Filling `known_spells` does not change an action, so the judge replayed the parent.

Five games still end at depth 1, to a kobold zombie, a bat, a coyote, a bat, and a newt. No game starves. The 20-square corpse cap is the change that raised the mean to 0.077.

## What might solve it

The note leaves that cap alone. It requires an uncommented `self.cast('force bolt', ...)` in `emergency_strategy` that runs only when energy is at least 5 and an adjacent monster makes `imminent_death_on_melee` true, and that monster is not a pet and not in `WEAK_MONSTERS`. The spell list has to be read once the role is known, or that cast cannot see the letter. Deleting the cast after a local game makes the iteration empty.

## Result

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). No code change.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Read the spell menu and deleted the cast.
