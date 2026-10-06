# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent bot played the 15 judge seeds and every game ended in death. Mean
progress was **0.114** (highest milestone averaged over the seeds). No game hit
a turn limit, so nothing stalled: each one ran until a monster, a trap, or a
poison killed the wizard.

| seed | milestone | depth | turns | cause of death |
|------|-----------|-------|-------|-----------------|
| 0 | Xp:9 | 1 | 50145 | poisoned by an orcish arrow |
| 1 | Xp:10 | 1 | 46006 | killer bee |
| 2 | Xp:8 | 1 | 34154 | bolt of fire |
| 3 | Xp:10 | 3 | 57042 | poisoned by an orcish arrow |
| 4 | Xp:2 | 2 | 2742 | goblin |
| 5 | Xp:10 | 1 | 55705 | giant bat |
| 6 | Xp:10 | 3 | 73840 | plains centaur |
| 7 | Xp:9 | 6 | 34611 | vampire bat |
| 8 | Xp:6 | 1 | 9957 | newt |
| 9 | Xp:11 | 3 | 69906 | invisible Mordor orc |
| 10 | Xp:4 | 2 | 6313 | kitten |
| 11 | Xp:8 | 4 | 23577 | pony |
| 12 | Xp:5 | 2 | 5011 | kobold lord |
| 13 | Xp:10 | 5 | 48694 | dwarf lord |
| 14 | Xp:8 | 1 | 32018 | bolt of cold |

Progress is a pure step function of the highest experience level reached:
Xp:2 = 0.018, Xp:4 = 0.024, Xp:5 = 0.029, Xp:6 = 0.037, Xp:8 = 0.075,
Xp:9 = 0.117, Xp:10 = 0.179, Xp:11 = 0.255. So one extra experience level is
worth roughly +0.06 to +0.13 on a single game.

## What is the problem

The kept XP gate (`experience_level >= 12`) keeps the wizard on the first Doom
level farming monsters for tens of thousands of turns. Progress is capped by
that farming: nine of fifteen games never got past the first level, and most
died in the Xp:8-Xp:11 band, one level or two short of the gate that would let
it descend. In other words the wizard is not out-explored, it is out-farmed, and
something kills it right before it can level up again.

Eight of the fifteen deaths are a monster the wizard simply cannot trade
blows with: killer bee, giant bat, vampire bat, plains centaur, pony, kitten,
dwarf lord, Mordor orc (plus a goblin and kobold lord at very low levels). The
wizard has few hit points and little melee damage, so a straight exchange with
a fast or hard-hitting monster kills it in a few rounds. Four further deaths
(orcish arrow poison x2, bolt of fire, bolt of cold) are ranged/trap, not melee.

The bot walks into these fights on purpose. `draw_monster_priority_positive`
draws a `+3` approach ring around every non-weak monster, and `goto_action`
gives `go_to` a priority of `1`, so the bot closes to striking distance. Melee
scores about `16`, which beats every flee ring, so once adjacent it always
swaps hits instead of retreating. Earlier attempts only strengthened the flee
rings and the Elbereth thresholds; that never helps, because melee outbids them
the moment the bot is adjacent. The fix has to stop the bot from *becoming*
adjacent, not to make it run once it already is.

## What might solve it

See `experiments.md`: score a monster by whether a straight melee exchange
costs more hit points than the hero actually has, and when it does, offer a
keep-away gradient instead of an approach ring.
