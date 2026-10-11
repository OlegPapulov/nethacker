# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The reference eval (`parent-eval.json`) ends every game below experience level 12, so the
bot never advances the farm milestone and never leaves the first floors.

Ends of the played games (cause of death, deepest level reached):

- seed 0: killed by a coyote, depth 4
- seed 1: killed by a dwarf lord, depth 1
- seed 2: killed by a bolt of fire, depth 1
- seed 3: killed by a fire ant, depth 1
- seed 4: killed by a goblin, depth 2
- seed 5: killed by a soldier ant, depth 1
- seed 6: killed by a hobbit, depth 3
- seed 7: poisoned by a rotted rothe corpse, depth 3
- seed 8: killed by a newt, depth 1
- seed 9: killed by an invisible Mordor orc, depth 3
- seed 10: killed by a kitten, depth 2
- seed 11: killed by a pony, depth 4
- seed 12: killed by a kobold lord, depth 2
- seed 13: killed by a dwarf lord, depth 5
- seed 14: killed by a bolt of cold, depth 1

## What is the problem

Two separate losses:

- Four games (0, 1, 5, 13) are killed in melee by a tough monster (a dwarf lord, a
  soldier ant, a coyote, a hill orc) after the wizard has thrown away its daggers. With
  no ranged attack left, the wizard walks up and trades blows, and a single bad exchange
  ends the game. These are the late, deep games, where the milestone has the most room to
  grow.

- The remaining games die early to a small monster (goblin, newt, kitten, pony, kobold
  lord, rothe-corpses, bolts), before the wizard ever learns to fight. Those are the short
  games and are the parent's already-tuned territory; no change here should disturb them.

The middle games (2, 3, 9, 14) reach experience level 8-11 and die to a monster that got a
hit in, while the wizard again has no ranged fallback once its daggers are spent.

## What might solve it

Give the wizard back a ranged attack for the phase of the game where it has already
thrown everything: cast force bolt, from experience level 10, on the first dungeon level,
at a monster that is not adjacent, whenever there is no throw to withhold. That is the
level of the cast the rules measure as a raise. See `experiments.md`.