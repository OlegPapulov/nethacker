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

## Result

- iteration 1: none not kept (gate:child identical to parent).

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

## Why it stopped

killed by a soldier ant (2 of 15).

## What is the problem

Mean progress is 0.077. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The usual stop is killed by a soldier ant. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. The last edit read the spell menu and then deleted the cast, so all 15 games replayed the parent. Filling `known_spells` is not a change. Call `parse_spellcast_view` once the role is known, and stop clearing `known_spells` in `_parse`. In `emergency_strategy`, leave an uncommented `self.cast('force bolt', ...)` that runs only when energy is at least 5 and an adjacent monster makes `imminent_death_on_melee` true, and that monster is not a pet and not in `WEAK_MONSTERS`. Do not cast at every adjacent glyph. Do not delete that cast after a local game. Do not hardcode a spell letter.

Edit `autoascend/` and exit. The judge measures that tree.

