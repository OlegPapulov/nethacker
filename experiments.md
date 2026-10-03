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

## Why it stopped

killed by a soldier ant (2 of 15).

## What is the problem

Mean progress is 0.077. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The usual stop is killed by a soldier ant. Leave the weak-hunger corpse walk capped at 20 squares. That cap raised the mean from 0.064 to 0.077. Do not edit it. `parse_spellcast_view` is never called, and `_parse` sets `known_spells` to an empty dict, so the force bolt block does not run. Call `parse_spellcast_view` once the role is known, and stop clearing `known_spells` inside `_parse`. Do not hardcode a spell letter. Leave that edit in the tree. Do not revert it.

Edit `autoascend/` and exit. The judge measures that tree.
- iteration 3: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Called `parse_spellcast_view()` after the role is known and stopped `_parse` clearing `known_spells`; the spell list is now read from the cast menu instead of a hardcoded letter. Fixed `cast()` so a diagonal is one compass action, not two letters (getdir completes on the first key, so 'ne' used to fire the spell north and then walk east). Score is unchanged at 0.077 because nothing casts yet; the edit is kept as prescribed.
- iteration 4: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Wired force bolt into `emergency_strategy` for the first time and measured 0.0532 against 0.0694 without it. The block targets "any adjacent monster glyph", which is also the wizard's own pet and an innocent lichen; a wizard has six energy against a cost of five and energy takes ~50 turns to return. Reverted, keeping only the refusal handling and the fixed aim.
- iteration 5: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Handled a refused cast (no turn is spent, so the strategy must wait) and two dressing/wear crashes. Zero errors across all fifteen seeds; the score is the parent's 0.077370 exactly.

## What the food investigation found

The wizard's worst losses are still `You faint from lack of food`, and instrumentation showed it eating nothing in 2,644 turns while standing next to corpses it had already found. The 50-turn rot window in `_is_corpse_editable` looks like the culprit, so it was measured: no check at all scores 0.029, a 500-turn window scores 0.0496, a 150-turn window scores 0.0572, and the parent's 50 scores 0.0774. Removing or widening it does not fix the starvation -- it just swaps fainting for `poisoned by a rotted gnome corpse`, because the wizard then eats corpses the game has already turned.

One trap worth recording: an early version of that experiment also dropped the parent's lizard/lichen exemption, which is load-bearing. Lichen corpses do not rot -- instrumented runs eat them thousands of turns after the kill and the game still reports them fresh -- and confusing that with the rot clock made the wizard throw away its safest food. The food path in `eat_corpses_from_ground` is now byte-identical to the parent.

The real limit is the supply of *fresh* corpses on dlvl 1, not the constant.
