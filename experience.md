# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note, but the kept iterations that built it tell the story. The
wizard parks on Doom floor 1-2 and farms xp until experience level 12 (the gate at
`experience_level >= 12` scores the same 0.114 as gates 11 and 14, so no seed ever reaches 12
while farming). The mean of 0.114 comes from a few strong seeds (seed 9 banks 0.255, seeds
1, 3, 5, 6 and 13 bank 0.179, seed 14 banks 0.117) plus a long tail of seeds that die before
level 10.

## What is the problem

The wizard "dies to almost anything that reaches melee range." It has few hit points, no usable
ranged attack of its own, and spends its whole game farming slow, safe monsters on the Doom
floors. The score is the highest milestone a game banks, so every seed's number is capped by the
level it reaches before its first death. Starvation is being handled (walk-and-eat corpses when
weak, latch onto dlvl 2 when fainting, cap corpse walks at 20 squares). The remaining lever is
raw xp income: seeds sit at a level boundary and die; they need a bit more safe xp to cross to
the next banked milestone (0.117 to 0.179, or 0.179 to 0.255).

## What might solve it

See `experiments.md`.