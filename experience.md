# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The 15 parent seeds all end in a death on the farm floors (Dungeons of Doom 1-6), never leaving the first
area, while the bot waits for experience level 12. The ends of the games, from the parent batch
(`/refs/parent-eval.json`):

- 5 reached `Xp:10`, then: killed by a giant bat; killed by a killer bee (twice); poisoned by a rotted
  rothe corpse; killed by a dwarf lord.
- 3 reached `Xp:11`, then: killed by a spotted jelly; killed by a housecat; killed by an invisible
  Mordor orc.
- 3 reached `Xp:8`, then: killed by a bolt of fire; killed by a pony; killed by a bolt of cold.
- 4 died before reaching `Xp:8`: killed by a goblin (`Xp:2`); killed by a kitten (`Xp:4`); killed by a
  kobold lord (`Xp:5`); killed by a newt (`Xp:6`).

## What is the problem

The milestone that moves the score is the experience level. The mean across the 15 seeds is 0.1328
(`Xp:10` in most games). The pattern in the deaths is not an exotic endgame: the killers are ordinary
farm-floor monsters (bat, bee, newt, kitten, pony, jelly, orc). They only become lethal after several
earlier fights have run the wizard's hit points down, and the bot never pauses to recover -- the
healing branches only fire at one third of max hit points (potions) and one sixth (prayer), so between
fights the wounded wizard simply walks into the next fight and trades blows until it dies. `Xp:11` is
worth 0.2548 against 0.1791 for `Xp:10` and 0.0745 for `Xp:8`, so rescuing even a few of these
accumulated-damage deaths would raise the mean.

## What might solve it

Local replays (public seeds) put the failure into two shapes. The games that die young (`Xp:2`-`Xp:6`)
reach `HUNGRY`-`WEAK`-`FAINTING` quickly after a few kills and collapse into food issues while fainting
next to a monster. The games that die late (`Xp:8`-`Xp:11`) trade blows in melee at low hit points:
the melee action is offered unconditionally against an adjacent monster, the defensive movement rings
only shape movement, and the pursuit fallback (priority 1) outbids the retreat cells (`-5`/`-10`), so a
wounded wizard walks straight into a bat, a killer bee, a kitten, a kobold lord, or a Mordor orc and
trades until it falls. Reaching `Xp:12` is worth 0.3326 against 0.2548 at `Xp:11`, so surviving those
last farm fights is the biggest single source of score.

See `experiments.md`.