# Next experiment

## Result

- iteration 1: 0.045 not kept. Decreases the mean by 0.032 (from 0.077 to 0.045). Packed fresh edible corpses into the pack and ate them from there. 4 of the 15 games ended in `poisoned by a rotted X corpse`.
- iteration 2: 0.046 not kept. Same idea with a hard cap of 3 corpses in the pack and a 1/3-capacity weight limit. Still 4 poisonings by rotted corpses.
- iteration 3: 0.066 not kept. Same idea plus an age gate: a packed corpse is only eaten while its recorded kill turn is less than 50 turns old. Poisonings gone, but the mean is still 0.011 below the parent.
- iteration 4: 0.077 not kept. Same as iteration 3, but the reserve is only packed when the pack holds no other food at all. The weak seeds improved less and the mean fell to 0.051.

No code change is kept. The tree matches `/refs/parent`; the judge table for it is 0.077370.

## Why it stopped

killed by a soldier ant (2 of 15), as in the parent.

## What is the problem

Mean progress is 0.077. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`. 5 of 15 games still die on depth 1, so the mean is set by a handful of long games.

## What might solve it

The corpse-larder idea is dead, and the traces say why.

1. **A pack is not a larder.** A corpse taints with age no matter where it is. `eatcorpse` computes `rotted = (monstermoves - age) / (10 + rn2(20))` and anything above 5 is tainted, so a corpse needs roughly 60-170 turns to become dangerous. Carrying it only hides it. The existing `_is_corpse_editable` 50-turn check for corpses on the floor is already on the safe side of that, which is why the parent is not poisoned. Any future corpse change must carry a kill-turn record with the corpse, the way `level.corpses_to_eat` does, or it will poison us.
2. **Starvation is real but the fix is not "carry corpses".** Traces show `You faint from lack of food` and seed 14 starving to death, but the deaths that cost the most were not food deaths: seed 14 went 0.117 -> 0.021 and seeds 6, 7, 9 dropped one or two XP levels purely because extra pack management and extra eating turns slowed the bot down.
3. **The pet eats the food.** On seed 14 the wizard's kitten eats the jackal corpses the bot kills (`The kitten eats a jackal corpse`), so the bot starves next to fresh corpses. Nothing in `ItemPriority` looks at `has_pet` when it decides what to pick up.
4. **Choking is a real cost of eating.** `choked on a food ration` and `choked on a lichen corpse` both end games, and eating one corpse costs 3-5 turns. Any "eat more" change has to pay for those turns.
5. **Spell parsing is still untried.** `parse_spellcast_view` is never called and `_parse` sets `known_spells` to an empty dict, so the force bolt block never runs. The wizard starts without a spellbook on these seeds (`CAST` answers `Never mind.`), so this only pays off once a spellbook is picked up, but the parser itself is still dead code and remains the cheapest untested lever. Leave the weak-hunger corpse walk capped at 20 squares; that cap raised the mean from 0.064 to 0.077.

Edit `autoascend/` and exit. The judge measures that tree.