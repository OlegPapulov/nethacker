# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

All fifteen judge games end before experience level 12, so the farm gate (leave
the first floors only at Xp 12) never pays off. The mean is 0.138.

The deaths, per the parent eval:

- Xp 11, on dlvl 1: killed by a dwarf lord (1), a fire ant (3), a soldier ant (5).
  These are one level short of the 0.333 Xp 12 milestone; a ranged kill before
  melee would have banked more.
- Low-XP deaths on deeper floors: a goblin at Xp 2 (4, dlvl 2), a kitten at Xp 4
  (10, dlvl 2), a kobold lord at Xp 5 (12, dlvl 2), a pony at Xp 8 (11, dlvl 4),
  a coyote at Xp 10 (0, dlvl 4), a hobbit at Xp 10 (6, dlvl 3), an invisible
  Mordor orc at Xp 11 (9, dlvl 3), a dwarf lord at Xp 10 (13, dlvl 5). These are
  below the farm floor: the staircase explorer follows a down staircase during
  the farm and strands the wizard next to deeper-floor spawns while it is still
  low level.
- Misc: killed by a bolt of fire (2, dlvl 1), a newt (8, dlvl 1), a bolt of cold
  (14, dlvl 1), poisoned by a rotted rothe corpse (7, dlvl 3).

## What is the problem

The bot does not actually stay on the first Dungeon level until Xp 12: the
staircase exploration takes it one (or more) floors down at low experience, and
it dies there instead of farming. Runs that do stay on dlvl 1 die in melee at
Xp 10-11, just before the level-12 gate.

## What might solve it

Keep the farm on the first floors for real: while the milestone is
BE_ON_FIRST_LEVEL, `explore_stairs` must not follow a down staircase that lands
deeper than the current farm target (`_xp_farm_level`, default dlvl 1). The
food-latch rescue (fainting, no corpse in reach -> dlvl 2) still works, because
that descent lands exactly on the farm target and stays allowed.