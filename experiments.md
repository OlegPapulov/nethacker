# Next experiment

## Result

- iteration 1: 0.114 not kept (parent, `wiz-hum-cha-mal`). The parent batch is the 15 seeds in `experience.md`; every run dies to a low-hit-point killing blow.

## Why it stopped

The wizard is a fragile human wizard with no usable ranged attack. It farms the first Doom levels for experience, starves on an exhausted level, and dies at Xp:2-11. The four worst seeds (goblin 2, kitten 4, kobold lord 5, newt 6) are starvation descents that end at single-digit hit points; the rest are arrows, wand bolts, bees, bats, centaurs, lords, and orcs landing the final hit while hp is already below the recovery line.

## What is the problem

`emergency_strategy` waits until `hitpoints < 6` before it prays at all (and healing potions, when the wizard even has one identified, wait until `< 8`). Every seed's cause of death is a 1-8 point attack that landed while the wizard was in exactly that no-man's-land. The parent's tuned prayer *cooldown* (500 turns low-hp, 400 fainting) is kept; the *trigger line* is what exposes the wizard.

## What might solve it

Raise the low-hit-point prayer trigger from `hitpoints < 6` to `hitpoints < 9` in `emergency_strategy`.

- One test that already exists is changed (`self.blstats.hitpoints < 6`), no action is added.
- The prayer cooldown (500 / 400) is untouched, so prayer still fires no more often than the measured parent; the change only *starts* the recovery a few hit points earlier, so the wizard carries a buffer into the next fight instead of fighting at 1-5 hp.
- This is not the measured-low prayer-wait test (3500): the cooldown numbers stay at 500 / 400, and `9` is not a nearby number to that change.
- It targets the common cause of every seed's death directly: earlier recovery means the final arrow / bee / bat / lord / orc / goblin hits a wizard with more hit points, so more seeds bank Xp:10-11 instead of Xp:8-9, and the four starvation seeds survive past the first descent.

Change the bot from the proposal above. The judge measures that tree.