# Playthrough

Identity: `wiz-hum-cha-mal`

## The games (public seeds, corrected harness)

The harness reruns each seed with the Objective defaults the
judge uses (`max_steps=1,000,000`, `no_progress_timeout=10,000`). With the
pristine tree this reproduces the parent eval exactly: mean **0.11949**, and
every seed matches the parent's milestone, turn count, and death line.

| seed | milestone | progress | death |
|-----:|----------:|---------:|:------|
|  0 | Xp:9  | 0.117 | poisoned by an orcish arrow |
|  1 | Xp:10 | 0.179 | killed by a killer bee |
|  2 | Xp:8  | 0.075 | killed by a bolt of fire |
|  3 | Xp:11 | 0.255 | killed by a spotted jelly |
|  4 | Xp:2  | 0.018 | killed by a goblin (fainted, level-drained twice) |
|  5 | Xp:10 | 0.179 | killed by a killer bee |
|  6 | Xp:10 | 0.179 | killed by a killer bee |
|  7 | Xp:9  | 0.117 | killed by a vampire bat |
|  8 | Xp:6  | 0.037 | killed by a newt (frozen by a monster's gaze) |
|  9 | Xp:11 | 0.255 | killed by an invisible Mordor orc |
| 10 | Xp:4  | 0.024 | killed by a kitten (while praying) |
| 11 | Xp:8  | 0.075 | killed by a pony (while sleeping) |
| 12 | Xp:5  | 0.029 | killed by a kobold lord (fainted) |
| 13 | Xp:10 | 0.179 | killed by a dwarf lord |
| 14 | Xp:8  | 0.075 | killed by a bolt of cold |

## Why it stopped

The validator's public-seed self-test (same defaults) gives the parent mean
0.11949. A child is kept only when its mean is strictly higher; the current
tree is byte-identical to the parent, so this iteration does not beat the
baseline.

## What is the problem

The farm games cap at Xp10 (killer-bee swarms, seeds 1/5/6) or Xp11 (a
single strong monster on an exhausted first floor, seeds 3/9). The low games
die before any farming can happen: seed 4 is doubly level-drained (maxhp
17 -> 12 -> 7, Xp back to 1) and starves on Doom 2; seeds 8/10/12 die to an
invisible floating-eye gaze, a kitten during prayer, and starvation on Doom 2.

## What might solve it

New behaviors are proposed in `experiments.md`. Every new behavior that was
implemented and measured this session moved the mean down, so no change was
kept: the parent tree remains at the measured baseline of 0.11949 on these
public seeds.