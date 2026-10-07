# Playthrough

Identity: `wiz-hum-cha-mal`

## The parent batch

Mean progress 0.114 across the 15 judge seeds. Seed 9 banks `Xp:11` (0.255),
seeds 1, 3, 5, 6 bank `Xp:10` (0.179), and the rest die around `Xp:8`
(0.0745) or `Xp:9` (0.117). Seed 14 dropped from 0.117 to 0.075 when the
leave-dlvl-1 gate was raised from Xp 8 to Xp 12: it used to descend and bank
`Xp:9`, and now it stays on dlvl 1 and dies at `Xp:8`.

## Why it stopped

Every game ends on Dlvl 1 or Dlvl 2. The bot farms the first Doom levels and
only leaves dlvl 1 once it banks `Xp:12`, which no seed ever reaches, so the
Gnomish Mines / Sokoban milestones (which are worth the `Dlvl:*` progression
values) are never banked. The score is therefore the peak experience level
reached while grinding the top levels.

The batch plateaus at a mean of 0.114. The measured jump in the progression
table is steep between `Xp:8` and `Xp:10` (+0.179 per leap), so runs that die
at `Xp:8` leave most of the score on the table. A run is held at `Xp:8` when
the dlvl 1 floor runs out of fresh monsters and the remaining corpses are
scarce (fresh corpses rot past the 50-turn window). The wizard grinds a
corpse-only food chain on dlvl 1 (the pack is restricted, so most food has to
be eaten straight off the floor) and dies to one of the early killers: a
melee it cannot win, a trap or poison step, or a faint inside the corpse hunt.

The biggest lever is food and the stall around it. When hunger reaches WEAK
the bot walks up to 20 squares to a corpse. When hunger reaches FAINTING the
latch sends it down to dlvl 2 only if no edible corpse is within 20 squares —
so a run that keeps failing to reach a corpse at distance 11–20 (monster
blocks the path, the corpse is gone, the walk re-races the rot window)
repeats the doomed walk instead of leaving, stays at `Xp:8`, and dies. That
is the stall that holds the batches of seeds back.

## What might solve it

See `experiments.md`.