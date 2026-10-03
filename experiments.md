# Next mutator experiment

Applied with this change.

## Why it stopped

Run 37110207188 did not score a bot. The gate rejected the tree as identical to the 0.077 parent.

## What is the problem

The operator did not rewrite `autoascend/`. The header told it to leave a cast and not restore the parent. The game rules told it that rewriting the two markdown files was the end of the job. The operator brief told it that a matching tree is discarded. It left the parent in place, and the notes were unchanged too.

One `evolve --iterations N` also freezes the note. The next iteration is not told that the previous tree was thrown away.

## What might solve it

The header and `GAME_RULES.md` now say the edit is an action in `autoascend/`, and an identical tree is not scored. Each iteration is its own `evolve`, and the next note starts with what the previous tree did. The survival edit is the depth-1 melee: cast force bolt when that melee would be fatal and the monster is not a pet or a weak monster, and otherwise move toward a door or a corridor. Leave the 20-square corpse cap alone.

## Result

- iteration 1: none not kept (gate:child identical to parent). The tree matched the parent, so the judge did not run.

## Result

- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077).

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

## Why it stopped

killed by a soldier ant (2 of 15).

## What is the problem

Mean progress is 0.077. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The usual stop is killed by a soldier ant. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Five games die on depth 1 by standing in a melee: a kobold zombie, a bat, a coyote, a bat, and a newt. A wizard loses that trade. In `emergency_strategy`, when `imminent_death_on_melee` is true for an adjacent monster that is not a pet and not in `WEAK_MONSTERS`, leave an uncommented `self.cast('force bolt', ...)` if energy is at least 5 and the spell is known, and otherwise move toward a door or a corridor. Do not cast at every adjacent glyph. Do not delete that cast. Call `parse_spellcast_view` once the role is known so the letter is real, and do not clear `known_spells` in `_parse`. Do not hardcode a spell letter.

Edit `autoascend/` and exit. The judge measures that tree.

