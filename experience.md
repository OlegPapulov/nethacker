# Playthrough

Identity: `wiz-hum-cha-mal`

## The batch

The judge plays 15 seeds. Progress is the highest milestone a game reaches. The
current tree scores a mean of **0.1195**. One seed per line, from
`/refs/parent-eval.json`:

| seed | milestone | progress | depth | turns | cause of death |
|-----:|-----------|---------:|------:|------:|----------------|
| 0  | Xp:9  | 0.1170 | 1 | 50145 | poisoned by an orcish arrow |
| 1  | Xp:10 | 0.1791 | 1 | 46006 | killed by a killer bee |
| 2  | Xp:8  | 0.0745 | 1 | 34154 | killed by a bolt of fire |
| 3  | Xp:11 | 0.2548 | 1 | 69782 | killed by a spotted jelly |
| 4  | Xp:2  | 0.0185 | 2 |  2742 | killed by a goblin |
| 5  | Xp:10 | 0.1791 | 1 | 56808 | killed by a killer bee |
| 6  | Xp:10 | 0.1791 | 1 | 55769 | killed by a killer bee |
| 7  | Xp:9  | 0.1170 | 6 | 34611 | killed by a vampire bat |
| 8  | Xp:6  | 0.0369 | 1 |  9957 | killed by a newt |
| 9  | Xp:11 | 0.2548 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | Xp:4  | 0.0242 | 2 |  6313 | killed by a kitten |
| 11 | Xp:8  | 0.0745 | 4 | 23577 | killed by a pony |
| 12 | Xp:5  | 0.0291 | 2 |  5011 | killed by a kobold lord |
| 13 | Xp:10 | 0.1791 | 5 | 48694 | killed by a dwarf lord |
| 14 | Xp:8  | 0.0745 | 1 | 32018 | killed by a bolt of cold |

The best games reach Xp:11 (seeds 3 and 9). The milestone alone determines the
score, so the game has to survive long enough to gain levels, not to descend.

## Why it stopped

- Four games (seeds 4, 8, 10, 12) die young, at experience level 2, 6, 4 and 5
  and on depth 1-2, to ordinary weak monsters (goblin, newt, kitten, kobold
  lord). Their progress, 0.018 to 0.037, drags the mean down the most: four seed
  scores of 0.117 (Xp:9) each would add about +0.012 to the mean.
- The single most common killer is the killer bee (seeds 1, 5 and 6, all Xp:10).
  A killer bee is fast and poisonous; a low-hit-point wizard that trades melee
  blows with one loses most of the time.
- The remaining mid game deaths are equally melee shaped: a spotted jelly, a
  vampire bat, a dwarf lord, a pony, an invisible Mordor orc, plus three deaths
  to ranged bolts (orcish arrow, bolt of fire, bolt of cold).
- No game ever leaves the first six dungeon levels. The batch is decided by
  early melee combat, not by the depth the bot reaches.

## What is the problem

A wizard has very few hit points and a poor melee score. Its strength is a
spell or a wand that deals damage from a distance. The parent fires ray wands
(`magic missile`, `fire`, ...) but its `is_offensive_usable_wand` test throws
away every beam wand, so a **wand of striking** is never used even though the
game lists it as a useful early find and a wizard often starts with one. When
no ray wand is in the pack, the wizard has nothing but melee, which is exactly
how the killer-bee and young-monster games end.

## What might solve it

See `experiments.md`: treat the beam wand of striking as an offensive wand so
the wizard can kill the fast melee threats from a distance.
