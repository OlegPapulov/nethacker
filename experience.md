# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.
Across those seeds the wizard's games end in four ways:

- Starvation on the Doom farm floor. The wizard eats the corpses it finds on dlvl 1,
  but that floor is exhausted quickly. It then starves ("You faint from lack of food")
  and, helpless while fainted, is killed by a weak monster -- a goblin, a kitten, a
  newt, a kobold lord. This ends the short games (seeds 4, 8, 10, 12) around Xp2-Xp6,
  and it is a factor in the longer ones as well.
- Fast or melee-strong monsters. The wizard banks experience on the farm floor but has
  no usable ranged attack below Xp10. A fast monster (a fire ant, a soldier ant) or a
  strong melee attacker (a dwarf lord, an invisible Mordor orc, a coyote, a hobbit)
  closes to melee range and kills it (seeds 0, 1, 3, 5, 6, 9, 13) at Xp10-Xp11.
- A rotted corpse. One longer game ends "poisoned by a rotted rothe corpse" after
  eating a corpse the bot still treated as fresh (seed 7).
- Bolt traps. Two short games end to "a bolt of fire" / "a bolt of cold" (seeds 2, 14).

## What is the problem

The score is the mean over the 15 seeds of the highest milestone a game reaches.
The parent banks Xp10-Xp11 on the Doom floors in its long games and never pushes past
that, and dies young in several others, so the mean (0.1379) is held down by the seeds
that never reach the farm floor at all.

## What might solve it

See `experiments.md`. The parent re-learns only its force bolt spellbook on the farm
floor; the change also re-learns the wizard's other usable spells.
