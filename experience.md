# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.

Reading the ends of the games (local runs, core seeds 1..15):

- Most games end early, on dungeon levels 1-3, against a single ordinary monster
  the wizard cannot beat in melee: a hobbit, a housecat, an iguana, a giant ant,
  a manes, a cave spider. The wizard is a weak melee fighter (poor AC, light
  weapon) and has no usable ranged attack, so the first monster that reaches it
  and rolls well ends the run. A few end to an unidentified wand of striking or
  a bolt of fire/cold from an unseen caster.
- One game ends to starvation when there is genuinely no reachable edible corpse.
- The one avoidable death: while polymorphed, the wizard is Overloaded and is
  killed without being able to fight back. When it is polymorphed -- here, by
  lycanthropy, which turns the wizard into a wererat (corpse weight 40, physical
  size tiny) on a timer -- NetHack rescales carrying capacity to the form, so
  the wizard's ordinary pack is suddenly more than three times what the tiny form
  can carry. `arrange_items` deliberately stands down while polymorphed, so
  nothing sheds weight; NetHack then refuses to fight ("You cannot fight while
  so heavily loaded") and to move ("You don't have enough stamina to move"), and
  the wizard dies in place. The item model cannot see this because the capacity
  it budgets against is the wizard's own, not the current form's.

## What might solve it

See `experiments.md`.
