# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The judge re-measures the 15 seeds on the tree that exits. `parent-eval.json` is the
baseline for the current tree.

## The games

Twelve of the fifteen games grind Doom levels 1 and 2 until a fast melee monster
(bat, killer bee, housecat, jelly, orc) or a ray (bolt of fire/cold, death ray)
finishes the wizard, banking `Xp:8`-`Xp:11`. Three games die in the first few
thousand turns (`Xp:2`-`Xp:6`).

Two patterns show up most often in the late games:

- The wizard holds low current hit points for long stretches (e.g. 25/87) while a
  fast monster grinds it down. It would write Elbereth only once the monster is
  already adjacent and hit points are already low, and the monster acts while the
  word is being written.
- Ray deaths (bolt of fire, bolt of cold, bolt of lightning, death ray) hit from
  range with no counter at all.

The change in this tree is a new mid-fight habit for a leveled wizard: once it
reaches experience level 10, it writes Elbereth while a fast, non-weak monster is
still a few squares out (clear line, distance 2-5), before it becomes adjacent, so
the word is already on the floor when the monster arrives. It leaves every game
below level 10 byte-identical, since the early games die before the gate.

Measured over the fifteen judge seeds with the local harness, every seed keeps the
parent progress (`Xp:2/6/8/10/11` in the same seats); the pre-engrave fires in the
late games and changes which monster lands the final blow on seeds 0, 7, and 9,
but it does not move any game to the next milestone tier. Mean stays 0.1328.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.

## What might solve it

See `experiments.md`.
