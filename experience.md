# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

15 of 15 games ended in death: 14 killed by a monster, 1 by starvation. No game was truncated, no
episode errored, and none reached the Amulet. The usual stop is no longer a single monster — the runs
are spread over ape, fire ant, lynx, rope golem, white unicorn, lizard, jackal, sewer rat, bat,
giant rat, kobold zombie, shopkeeper and more. **0 of 15 are killed by a wolf** (was 2 of 15).

Mean progress **0.06431** (parent 0.06242). Milestones reached: Xp:9 (3 games), Xp:8 (6), Xp:7 (1),
Xp:6 (1), Xp:5 (1), Xp:4 (1), Xp:3 (1), Xp:2 (1).

| seed | progress | turns | depth | stop |
| --- | --- | --- | --- | --- |
| 0 | 0.074535952738840144 | 27740 | 2 | killed by an ape |
| 1 | 0.11704996473565571 | 21697 | 3 | killed by a fire ant |
| 2 | 0.074535952738840144 | 24862 | 5 | killed by Mr. Picq; the shopkeeper |
| 3 | 0.074535952738840144 | 19861 | 2 | killed by an invisible gnome king |
| 4 | 0.01847840456172601 | 2644 | 1 | killed by a kobold zombie |
| 5 | 0.036887590648350246 | 8788 | 1 | killed by a sewer rat |
| 6 | 0.11704996473565571 | 27730 | 5 | killed by a lynx |
| 7 | 0.11704996473565571 | 34603 | 5 | killed by a rope golem |
| 8 | 0.020811635819743549 | 4142 | 1 | killed by a giant rat |
| 9 | 0.074535952738840144 | 25313 | 3 | killed by a jackal |
| 10 | 0.074535952738840144 | 29898 | 4 | killed by a lizard |
| 11 | 0.036887590648350246 | 12486 | 1 | killed by a jackal |
| 12 | 0.024160136550546978 | 4917 | 1 | killed by a bat |
| 13 | 0.074535952738840144 | 31848 | 3 | killed by a white unicorn |
| 14 | 0.029108986017138745 | 7795 | 1 | died of starvation |

Official result file: `/tmp/eval.json` (`--evaluation-id local`). Compare with `/refs/parent-eval.json`.

## What the change was

Food handling. The parent only ever ate a corpse it was already standing on, so the wizard fainted
53-208 times per game. The bot now walks to the nearest safe corpse and eats it once it is WEAK.
See `experiments.md` for the hypothesis, the code, and the five rejected variants.

## What it moved, and what it did not

It moved hunger out of the death column almost entirely:

- faints: 53-208 per game -> **0** (measured on seeds 0, 4, 13);
- seeds reaching depth >= 2: 6/15 -> **9/15**; depth >= 3: 5/15 -> **7/15**;
- mean turns survived: 17138 -> **18955**; seed 13 went from 5206 turns to 31848;
- the mean score itself only 0.06242 -> 0.06431, because the score is set by how deep the lucky runs
  get and by the first monster met on depth 1.

## What is the problem now

1. **Still one starvation death (seed 14).** The cause is not that food is missing from the level —
   tracing it shows 7 corpses recorded, all reachable, all rejected by the 50-turn rule in
   `_is_corpse_editable` because we get hungry long after we killed the monster. Eating them anyway
   works until the corpse is rotted and poisonous (3 games died that way when measured). The fix is to
   eat *promptly*: take the corpse of the monster we just killed, while it is fresh.
2. **Early melee on depth 1.** 6 of 15 games die before leaving the first floor to a jackal, rat,
   bat, kobold zombie or goblin, often inside 3000 turns. A fragile wizard that trades hits with
   monsters loses a damage race; distance, doors and fleeing are what it needs instead.

## What might solve it

Item 1 first (it is small, food again, and one death is a whole seed), then item 2: make the combat
heuristic refuse the fights a human wizard should not accept rather than tuning hunger thresholds
again. See `experiments.md`.