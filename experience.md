# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## Game-end analysis of the parent run

Mean progress 0.1144 over 15 seeds. Nobody ascends; every game ends in a fight.
The deadliest enemy is not a trap or a special feature but free melee: when a
fast monster stands next to the wizard, `melee_monster_priority` keeps worth 16
even at critical hit points, and the wizard trades blows with a monster that
always takes its turn first.

Per-seed deaths:

| seed | score | milestone | turns | depth | cause |
|-----:|------:|-----------|------:|------:|-------|
| 0 | 0.117 | Xp:9  | 50145 | 1 | poisoned by an orcish arrow |
| 1 | 0.179 | Xp:10 | 46006 | 1 | killed by a killer bee |
| 2 | 0.075 | Xp:8  | 34154 | 1 | killed by a bolt of fire |
| 3 | 0.179 | Xp:10 | 57042 | 3 | poisoned by an orcish arrow |
| 4 | 0.019 | Xp:2  |  2742 | 2 | killed by a goblin |
| 5 | 0.179 | Xp:10 | 55705 | 1 | killed by a giant bat |
| 6 | 0.179 | Xp:10 | 73840 | 3 | killed by a plains centaur |
| 7 | 0.117 | Xp:9  | 34611 | 6 | killed by a vampire bat |
| 8 | 0.037 | Xp:6  |  9957 | 1 | killed by a newt |
| 9 | 0.255 | Xp:11 | 69906 | 3 | killed by an invisible Mordor orc |
| 10 | 0.024 | Xp:4 |  6313 | 2 | killed by a kitten |
| 11 | 0.075 | Xp:8 | 23577 | 4 | killed by a pony |
| 12 | 0.029 | Xp:5 |  5011 | 2 | killed by a kobold lord |
| 13 | 0.179 | Xp:10 | 48694 | 5 | killed by a dwarf lord |
| 14 | 0.075 | Xp:8 | 32018 | 1 | killed by a bolt of cold |

Five of the fifteen deaths (seeds 1, 5, 7, 10, 11) are caused by the exact set
of monsters `is_monster_faster` recognises: killer bee, giant bat, vampire bat,
kitten and pony. These are the monsters that "take a turn before the wizard
takes a turn"; the wizard dies trading melee with them instead of stepping back.

## What is the problem

When a monster is next to the wizard and the wizard is nearly dead, the rules
codified in `imminent_death_on_melee` (`hp <= 8`, `hp <= 16` for pets and
insects) already say "do not stand there": the positive approach ring is
suppressed and a punishing negative ring is drawn around the monster. But
`melee_monster_priority` adds 15 to melee for any healthy wizard and again for
any fast monster, so that +15 is higher than the escape gradient and the wizard
attacks anyway. A fast monster strikes first and kills it.

## What might solve it

See `experiments.md`.