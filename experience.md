# Playthrough

Identity: `wiz-hum-cha-mal`

## What the games do

The bot farms the first Doom level. It explores the floor, fights what it can
in melee (a blessed +1 quarterstaff, a +15 melee bonus while it has more than
eight hit points or is faster than the monster), eats corpse and ration food,
quaffs only potions it has identified, and prays when its hit points fall low.
The farm gate is experience level 12: below that it stays on the first level,
except that when it is fainting with no edible corpse within 20 squares it
latches onto the second level instead. A wizard starts with no throwing ammo,
so the only ways it can fight at range are its wands and its spells.

## Why the games stop

Fifteen seeds, ordered by the milestone each one reaches:

- seed 9  `Xp:11` -- farms to level 11 on the first and second levels, then is
  killed by an invisible Mordor orc.
- seed 1  `Xp:10` -- killed by a killer bee.
- seed 3  `Xp:10` -- poisoned by an orcish arrow.
- seed 5  `Xp:10` -- killed by a giant bat.
- seed 6  `Xp:10` -- killed by a plains centaur.
- seed 13 `Xp:10` -- its weapons are stolen by a mountain nymph; killed by a dwarf lord.
- seed 0  `Xp:9`  -- poisoned by an orcish arrow.
- seed 7  `Xp:9`  -- killed by a vampire bat.
- seed 2  `Xp:8`  -- killed by a bolt of fire.
- seed 11 `Xp:8`  -- killed by a pony.
- seed 14 `Xp:8`  -- killed by a bolt of cold.
- seed 8  `Xp:6`  -- throws its last dagger at a floating eye, then walks into
  the eye's square, is paralysed by its gaze, and is bitten to death by a newt.
- seed 12 `Xp:5`  -- runs out of food on the second level and is killed by a kobold lord.
- seed 10 `Xp:4`  -- killed by a kitten.
- seed 4  `Xp:2`  -- killed by a goblin after 2,742 turns.

The early deaths (seeds 4, 8, 10, 12) are food, a weak melee or an unlucky
monster. The level-10 games all die just short of the next milestone, and their
killers are exactly the monsters a wizard would rather not trade blows with: a
killer bee, a bat, a centaur, a dwarf lord. The one thing the wizard never does
is cast a spell, even though it knows `force bolt` in every game and has more
than seventy energy by level 10.

## What changed

One behaviour was added: from experience level 10 on, while the wizard is on
the first Doom level, it may cast `force bolt` at a non-weak monster that is two
to eight squares away along a clear line, instead of only walking up and
meleeing. Everything below level 10 is untouched, so the games that die young
are byte-for-byte the same. The effect is that seed 3 now reaches `Xp:11`
instead of `Xp:10`; seeds 5 and 6 keep `Xp:10` with different turn counts; the
other twelve games are unchanged. The mean rises from 0.114 to 0.119.

## What might solve it

See `experiments.md`.
