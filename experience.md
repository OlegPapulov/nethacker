# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

`experience.md` in the parent batch is empty of ends ("The parent batch is not
in this note"), so the only record of how the games ended is
`/refs/parent-eval.json` (the 15 trajectories the judge played on the parent).
The file states these ends, and only these:

| seed | end                                           | milestone | depth |
|------|-----------------------------------------------|-----------|-------|
| 0    | killed by a giant bat                          | Xp:10     | 2     |
| 1    | killed by a killer bee                         | Xp:10     | 1     |
| 2    | killed by a bolt of fire                       | Xp:8      | 1     |
| 3    | killed by a spotted jelly                      | Xp:11     | 1     |
| 4    | killed by a goblin                             | Xp:2      | 2     |
| 5    | killed by a killer bee                         | Xp:10     | 1     |
| 6    | killed by a housecat                           | Xp:11     | 6     |
| 7    | poisoned by a rotted rothe corpse              | Xp:10     | 3     |
| 8    | killed by a newt                               | Xp:6      | 1     |
| 9    | killed by an invisible Mordor orc              | Xp:11     | 3     |
| 10   | killed by a kitten                             | Xp:4      | 2     |
| 11   | killed by a pony                               | Xp:8      | 4     |
| 12   | killed by a kobold lord                        | Xp:5      | 2     |
| 13   | killed by a dwarf lord                         | Xp:10     | 5     |
| 14   | killed by a bolt of cold                       | Xp:8      | 1     |

The mean is 0.1328. Eight seeds stop at Xp:10-11 (0.179-0.255); the rest stop
far lower (Xp:2-8). Several of the ends are weak monsters (newt, kitten, pony,
goblin) finishing a wizard that was already worn down, and two ends are a ray
("killed by a bolt of fire"/"killed by a bolt of cold") at depth 1 while the
wizard is only Xp:8.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game
reaches. Experience level is the milestone that moves this score.

## What might solve it

See `experiments.md`.
