# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

All fifteen parent games end in a death on the Dungeons of Doom. Nothing reaches
Gehennom, and no seed reaches the Gnomish Mines on purpose. The mean is 0.114.

| seed | progress | milestone | cause of death | turns | max depth |
|---|---|---|---|---|---|
| 0 | 0.1170 | Xp:9 | poisoned by an orcish arrow | 50145 | 1 |
| 1 | 0.1791 | Xp:10 | killed by a killer bee | 46006 | 1 |
| 2 | 0.0745 | Xp:8 | killed by a bolt of fire | 34154 | 1 |
| 3 | 0.1791 | Xp:10 | poisoned by an orcish arrow | 57042 | 3 |
| 4 | 0.0185 | Xp:2 | killed by a goblin | 2742 | 2 |
| 5 | 0.1791 | Xp:10 | killed by a giant bat | 55705 | 1 |
| 6 | 0.1791 | Xp:10 | killed by a plains centaur | 73840 | 3 |
| 7 | 0.1170 | Xp:9 | killed by a vampire bat | 34611 | 6 |
| 8 | 0.0369 | Xp:6 | killed by a newt | 9957 | 1 |
| 9 | 0.2548 | Xp:11 | killed by an invisible Mordor orc | 69906 | 3 |
| 10 | 0.0242 | Xp:4 | killed by a kitten | 6313 | 2 |
| 11 | 0.0745 | Xp:8 | killed by a pony | 23577 | 4 |
| 12 | 0.0291 | Xp:5 | killed by a kobold lord | 5011 | 2 |
| 13 | 0.1791 | Xp:10 | killed by a dwarf lord | 48694 | 5 |
| 14 | 0.0745 | Xp:8 | killed by a bolt of cold | 32018 | 1 |

The wizard levels on the Doom floors and dies there. Six seeds bank Xp:10
(0.179), one banks Xp:11 (0.255), and four stop at or below Xp:6 for a combined
0.109 of the total 1.717 -- those four alone cost about 0.041 of the mean.
Seeds 4, 10 and 12 die on depth 2 between 2,742 and 6,313 turns, which is far
below the farm target of depth 1; they are the fainting latch sending a starving
wizard down a floor, and the floor kills it.

Three ways to die show up over and over:

- Missiles and spells: two orcish arrows, a bolt of fire, a bolt of cold. Five
  seeds end under something that was fired from a distance, and none of those
  attacks were ever answered from a distance.
- Fast bodies: a killer bee, a giant bat, a vampire bat, a pony. A faster
  monster takes a turn before the wizard takes a turn.
- Ordinary melee on a floor the wizard walked into: goblin, kobold lord, newt,
  kitten, dwarf lord, plains centaur, invisible Mordor orc.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game
reaches.

The wizard has exactly one answer to a monster: walk into melee range and hit
it. `melee_monster_priority` is worth 16 whenever hit points are above 8, and
16 beats every square the movement heatmap can offer (it peaks around +12), so
as soon as anything is adjacent the wizard trades blows until it is under 8 hit
points. Its only other attack is a wand, and `get_potential_wand_usages` writes
`priority = priority - 15` on every zap before it is compared with anything.
Against an ordinary monster a wand of magic missile or fire therefore scores
10 - 15 = -5, which is below a neutral square (0), below `goto_action` (+1), and
far below a step toward safety. The bot identifies wands -- `wand_engrave_identify`
runs inside `gather_items` -- and then never fires one. The Items paragraph of
the game rules calls a wand of striking and a wand of magic missile useful early
finds, and a spell that does damage from a distance is exactly what a wizard with
few hit points is for.

## What might solve it

See `experiments.md`.
