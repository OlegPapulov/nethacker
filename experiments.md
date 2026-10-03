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
