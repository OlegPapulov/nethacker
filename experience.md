# Playthrough

Identity: `wiz-hum-cha-mal`

## The ends of the fifteen judge seeds

The parent batch (mean 0.1144) scored these milestones, each death a killing blow at low hit points:

- seed 0: Xp:9, depth 1, poisoned by an orcish arrow
- seed 1: Xp:10, depth 1, killed by a killer bee
- seed 2: Xp:8, depth 1, killed by a bolt of fire (wand-carrying monster, ranged)
- seed 3: Xp:10, depth 3, poisoned by an orcish arrow
- seed 4: Xp:2, depth 2, killed by a goblin
- seed 5: Xp:10, depth 1, killed by a giant bat
- seed 6: Xp:10, depth 3, killed by a plains centaur
- seed 7: Xp:9, depth 6, killed by a vampire bat
- seed 8: Xp:6, depth 1, killed by a newt
- seed 9: Xp:11, depth 3, killed by an invisible Mordor orc
- seed 10: Xp:4, depth 2, killed by a kitten
- seed 11: Xp:8, depth 4, killed by a pony
- seed 12: Xp:5, depth 2, killed by a kobold lord
- seed 13: Xp:10, depth 5, killed by a dwarf lord
- seed 14: Xp:8, depth 1, killed by a bolt of cold (ranged)

## Why it stopped

The wizard farms the first Doom levels until experience level 12 and never gets there; every run ends with a monster (or arrow, or wand bolt) landing the final hit while the wizard is in single-digit hit points. Nobody dies to a big single hit or to a trap; every cause of death is a normal attack that arrived while the wizard was already below its recovery line.

The four worst seeds (2, 4, 5, 6) starve on an exhausted level one, latch to depth 2 for food, and are killed there by weak monsters (goblin, kitten, kobold lord, newt) while at a handful of hit points. The eleven better seeds reach Xp:8-11 on the Doom floors and then die the same way: the last arrow, bee, bat, centaur, lord, or orc hits them between 1 and 8 hit points.

## What is the problem

The recovery line is too low. `emergency_strategy` only prays once hit points drop below 6 (or quaffs an *identified* healing potion below 8). Below that line an unlucky monster hit of 1-8 is lethal, and a wizard sitting on a farmed floor spends a large share of its time in the 1-9 range between corpse meals. The deaths are not caused by one wrong fight; they are caused by arriving at fights with no buffer.

## What might solve it

Start the heal/pray recovery a few hit points earlier, so the wizard is rarely at 1-5 hp when the next attack lands. The prayer cooldown already caps how often prayer can fire, so this adds buffer without adding god-peril or new actions.

See `experiments.md`.