# Playthrough

Identity: `wiz-hum-cha-mal`

## The games

The judge plays the 15 seeds after you exit; the numbers below are from replaying
those same seeds locally through the arena's own `run_prepared` entry point, which
reproduces the parent eval (`/refs/parent-eval.json`) exactly on unmodified code.

A wizard starts with `force bolt` and one random spell. It farms the first Doom
floor for experience, only latching down to dlvl 2 once it is fainting and no fresh
corpse is in reach. Progress is the *highest* milestone a game ever banks, so the
longer a run survives farming, the higher its score.

The parent runs end the same way almost every time: the wizard reaches
experience level 8-11 on the Doom floors and then dies a close one -- three times to
killer bees, once to a spotted jelly, once to a dwarf lord, once to a pony, once to a
bolt of fire, once to a bolt of cold, once to an orcish arrow, once to a bat, once to
an invisible Mordor orc. The early deaths (a goblin, a kitten, a kobold lord, a newt)
are the fainting-latch descent: the wizard is already at a sliver of hit points when
it reaches the new level and anything there finishes it. Starvation, not combat, is
the treshold that decides how many levels a run banks -- every turn spent walking or
waiting leaks food, so an exhausted dlvl 1 is a countdown.

## What changed

The one behavior added: `select_skill_to_upgrade` now spends a level-up's skill point
on the skill of the weapon the wizard actually holds. Before, the point went to
whichever of the two offered melee skills the spellbook menu happened to list first,
so it alternated between the held quarterstaff and the off-hand dagger -- half the
skill points went to damage rolls only the staff contributes to. Replaying the
fifteen seeds with this change kept every seed on the same milestone, and lifted
three of them one experience level higher: seed 0 from Xp9 to Xp10, seed 6 from Xp10
to Xp11, seed 7 from Xp9 to Xp10. Mean 0.133 against the parent's 0.119.

## Why it stopped

The judge measures the tree just before the parent's batch closes it out. The fifteen
replayed seeds under the new tree are in `experiments.md`; the mean is strictly
higher than the parent's on the same seeds, so the tree was kept.

## What might solve it

See `experiments.md` for the proposal behind this change and the next step.