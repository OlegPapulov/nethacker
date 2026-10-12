# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The games that set this score all end on the first dungeon levels. None of
them get past the farm that they are supposed to grind until experience level
12.

The bot loses for the causes the rules list for these floors:

- **Food.** The first floor is exhausted long before level 12. Corpses stop
  being edible once they rot past the freshness window, and dlvl 1 stops
  renewing its weak, edible monsters, so the wizard spends long stretches at
  hunger WEAK/FAINTING. While fainting it has no hit-point regeneration, and
  it dies in melee at a fraction of its max hit points. Several games end
  while helpless from starvation after 30k-90k turns on the first floor.
- **A weak melee.** The wizard has no usable ranged attack once its thrown
  ammunition runs out, so it trades blows with whatever reaches it. As the
  player levels, the first floor's monster spawns scale up (ants, a dwarf
  lord, an orc), and those melee trades are the deaths that end the runs at
  Xp 10 and Xp 11, just short of the level-12 gate.
- **A trap.** A bolt trap on these floors throws fire or cold. A starved,
  half-hit-point wizard triggers one and dies.
- **Poison.** A rotten corpse on these floors poisons the wizard. Games that
  misjudge a rotted corpse (the parent's freshness window is tuned and load-
  bearing) end poisoned.

The score never moves past Xp 11 because no game survives the melee long
enough or eats well enough to bank level 12 on the Doom floor.

## What is the problem

The mean is the highest milestone per seed. The accepted games are capped at
Xp 10-11 by melee deaths on the exhausted first floor, a level below the gate
that is worth 0.3326.

## What might solve it

The wizard's only ranged attack -- force bolt, allowed from experience level
10 on the first dungeon level -- is the tool the rules point at. It costs no
hit points and reaches a monster that cannot be reached in melee. Enabled
reliably, it lets the late games soften the scaled-up spawns before they
reach melee range, and it does not touch the games that die young.

See `experiments.md`.