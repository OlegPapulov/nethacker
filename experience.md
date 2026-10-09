# Playthrough

Identity: `wiz-hum-cha-mal` (chaotic male human wizard).

The judge plays the 15 seeds after exit; the parent batch below is the
reference the child has to beat. Progress is the highest milestone a game
reaches, taken over all seeds. Every game ends in death: no game ascends and
no game stalls out. The parent mean is 0.114 (0.1195 on the recorded run).

## The games

| seed | milestone | score  | max depth | turns  | stopped by |
|------|-----------|--------|-----------|--------|------------|
| 0  | Xp:9  | 0.1170 | 1 | 50145 | poisoned by an orcish arrow |
| 1  | Xp:10 | 0.1791 | 1 | 46006 | killed by a killer bee |
| 2  | Xp:8  | 0.0745 | 1 | 34154 | killed by a bolt of fire |
| 3  | Xp:11 | 0.2548 | 1 | 69782 | killed by a spotted jelly |
| 4  | Xp:2  | 0.0185 | 2 | 2742  | killed by a goblin |
| 5  | Xp:10 | 0.1791 | 1 | 56808 | killed by a killer bee |
| 6  | Xp:10 | 0.1791 | 1 | 55769 | killed by a killer bee |
| 7  | Xp:9  | 0.1170 | 6 | 34611 | killed by a vampire bat |
| 8  | Xp:6  | 0.0369 | 1 | 9957  | killed by a newt |
| 9  | Xp:11 | 0.2548 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | Xp:4  | 0.0242 | 2 | 6313  | killed by a kitten |
| 11 | Xp:8  | 0.0745 | 4 | 23577 | killed by a pony |
| 12 | Xp:5  | 0.0291 | 2 | 5011  | killed by a kobold lord |
| 13 | Xp:10 | 0.1791 | 5 | 48694 | killed by a dwarf lord |
| 14 | Xp:8  | 0.0745 | 1 | 32018 | killed by a bolt of cold |

## Why it stopped

The wizard dies. The deaths fall into four groups.

### 1. Fast monsters win the melee (seeds 1, 5, 6, 7, 10, 11)

Six games are ended by a monster that takes its turn before the wizard
(`is_monster_faster`): three killer bees, a vampire bat, a kitten, a pony. The
melee heuristic gives the wizard's attack a bonus of `+15` exactly when the
monster is faster, so the wizard always trades blows with the one kind of
monster it cannot out-run. The bee deaths all happen on Dlvl 1 between Xp 9 and
Xp 10; the bat drain (seed 7) is one level deeper.

### 2. Starvation cascades (seeds 4, 8, 10, 12)

These are the worst games (Xp 2 to Xp 6). Once the edible corpses on Dlvl 1 are
gone the wizard faints, hit points drain, and the next anything kills it: a
goblin, a newt, a kitten, a kobold lord. Seeds 4, 10 and 12 reached Dlvl 2
through the fainting farm latch and still died there, which says the problem is
food, not the level.

### 3. Ranged and reflected damage (seeds 0, 2, 14)

An orcish arrow (poison) and two elemental bolts. These are losses the wizard
does not see coming and cannot trade against.

### 4. Losing the open-room brawl (seeds 3, 9, 13)

The three longest games (Xp 10-11, 48k-70k turns) end to a stronger monster -
a spotted jelly that splits, an invisible Mordor orc, a dwarf lord - after the
wizard has spent its whole run on the first floors. In an open room several
monsters reach the wizard every turn; the wizard stands and hits back.

## What is the problem

Progress is the highest achievement, and `Xp:9` already scores 0.117 while the
top of the range the parent reaches is `Xp:11` at 0.255. The mean is held down
by the low games: the four starvation games (0.018-0.074) and the four difficult
deaths on the first floor (seeds 2, 8, 14 + the high-Xp swarm deaths). Any
behaviour that turns even a few early deaths into a deeper, higher-Xp run moves
the mean.

The common thread in the mid/high games (1, 3, 5, 6, 9, 13) is the wizard
standing in the open, surrounded by more than one monster, and trading one
attack for two or three incoming hits. The first tip says exactly this: a fight
in a doorway or a corridor lets one monster hit, an open room lets several.
Nothing in the bot chooses the ground of a fight -- the completed corridor
priority map in `combat/fight_heur.py` is still commented out and the wizard
never steps into a doorway on purpose.

The fast-monster and starvation clusters are fenced off by the six measured
tests in `GAME_RULES.md` (melee `+15`, the fainting farm latch, the corpse
walk), so the uncovered, tip-backed behaviour is to fight from a chokepoint.

## What might solve it

See `experiments.md`.
