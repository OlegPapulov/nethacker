# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

All fifteen parent games stop the same way: the wizard dies in the dungeon. The
judge reports `status: completed`, `error: null` and a non-null `cause_of_death`
for every seed, so no seed stalls, panics into the idle fallback, or runs out of
action budget -- every game plays until the character is dead, and the score each
seed reports is the best milestone it had already banked before it died
(`arena/progress.py` keeps `max` over the whole run, so a death never gives a
milestone back).

| seed | progress | milestone | max depth | turns | cause of death |
|---|---|---|---|---|---|
| 0 | 0.1170 | Xp:9 | 1 | 50,145 | poisoned by an orcish arrow |
| 1 | 0.1791 | Xp:10 | 1 | 46,006 | killed by a killer bee |
| 2 | 0.0745 | Xp:8 | 1 | 34,154 | killed by a bolt of fire |
| 3 | 0.1791 | Xp:10 | 3 | 57,042 | poisoned by an orcish arrow |
| 4 | 0.0185 | Xp:2 | 2 | 2,742 | killed by a goblin |
| 5 | 0.1791 | Xp:10 | 1 | 55,705 | killed by a giant bat |
| 6 | 0.1791 | Xp:10 | 3 | 73,840 | killed by a plains centaur |
| 7 | 0.1170 | Xp:9 | 6 | 34,611 | killed by a vampire bat |
| 8 | 0.0369 | Xp:6 | 1 | 9,957 | killed by a newt |
| 9 | 0.2548 | Xp:11 | 3 | 69,906 | killed by an invisible Mordor orc |
| 10 | 0.0242 | Xp:4 | 2 | 6,313 | killed by a kitten |
| 11 | 0.0745 | Xp:8 | 4 | 23,577 | killed by a pony |
| 12 | 0.0291 | Xp:5 | 2 | 5,011 | killed by a kobold lord |
| 13 | 0.1791 | Xp:10 | 5 | 48,694 | killed by a dwarf lord |
| 14 | 0.0745 | Xp:8 | 1 | 32,018 | killed by a bolt of cold |

## What is the problem

Mean progress is 0.114. Three facts describe the fifteen ends:

1. **Experience level is the whole score.** For every one of the fifteen seeds
   the reported progress equals that seed's `Xp:` milestone exactly -- the
   deepest floor any seed ever banked is `Dlvl:6` (0.0354) on seed 7, which is
   still below the `Xp:6` (0.0369) that seed already had. The wizard farms the
   first Doom level until it dies; nine seeds never leave Doom:1 at all, and the
   depths above 1 (max 6) come from trapdoor falls, not from walking down
   stairs. Anything that keeps the wizard alive long enough to gain one more
   experience level moves the mean; anything that only moves it down a corridor
   does not.

2. **Four games are short, eleven are long, all fifteen end in melee or in a
   projectile.** Seeds 4, 10, 12 and 8 die inside 10,000 turns at Xp:2-6 and
   stop the mean at 0.018-0.037. The other eleven run 23k-74k turns and stop at
   Xp:8-11. Eleven deaths are a monster standing next to the wizard (killer bee,
   giant bat, plains centaur, vampire bat, newt, invisible Mordor orc, kitten,
   pony, kobold lord, dwarf lord, goblin); four are attacks the wizard cannot
   answer at range (two poisoned orcish arrows, a bolt of fire, a bolt of cold).
   A wizard has few hit points and no ranged answer, so every one of these is
   the same end: the wizard is adjacent to something that out-damages it.

3. **In several of those fights the wizard is not fighting at all -- it is
   standing still on its own Elbereth engraving.** `fight_heur.elbereth_action`
   offers the engrave only when a non-weak monster is already adjacent and
   hitpoints are under 30 (`combat/fight_heur.py:201-226`), which is exactly
   the middle of a losing fight. Once `engraving_below_me == 'elbereth'`,
   `fight_heur.py:245-246`, `:257-258` and `:195-196` give every melee, ranged
   and zap action `-100` priority, while `wait_action`
   (`combat/fight_heur.py:229-234`) returns `30 - 40 * hp/max` for doing nothing.
   At the hitpoints where the wizard is in danger that wait beats everything
   else on the board -- including the retreat rings from
   `draw_monster_priority_negative`, which top out at +10 -- so the wizard
   stands on the engraving and takes the hits until it dies
   (`agent.py:1255-1259` is the wait branch; `agent.py:1251-1254` writes the
   engraving). Elbereth only turns away undead; it does not turn away a killer
   bee, a plains centaur, a pony or an invisible Mordor orc, and those are what
   killed this wizard. The engraving cannot end the fight (the wizard deals no
   damage while waiting), cannot be left at the hitpoints where it matters, and
   its only beneficiary in the parent batch -- the undead vampire bat on seed 7
   -- died to that bat anyway.

## What might solve it

See `experiments.md`: one change, and only one.
