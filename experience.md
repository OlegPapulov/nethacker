# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

2 of 15 games stopped at killed by a soldier ant. Mean progress 0.077. This is the parent tree
(`/refs/parent`), re-measured this iteration: all 15 seeds came back identical to
`/refs/parent-eval.json`, mean 0.077370.

| seed | progress | turns | stop |
| --- | --- | --- | --- |
| 0 | 0.07453595273884014 | 27750 | killed by an Uruk-hai |
| 1 | 0.11704996473565571 | 21697 | killed by a fire ant |
| 2 | 0.07453595273884014 | 24862 | killed by Mr. Guizengeard; the shopkeeper |
| 3 | 0.07453595273884014 | 20368 | killed by a soldier ant |
| 4 | 0.01847840456172601 | 2644 | killed by a kobold zombie |
| 5 | 0.11704996473565571 | 29992 | killed by a giant beetle |
| 6 | 0.07453595273884014 | 27825 | killed by a soldier ant |
| 7 | 0.07453595273884014 | 24393 | killed by a wand |
| 8 | 0.036887590648350246 | 9957 | killed by a newt |
| 9 | 0.11704996473565571 | 26641 | killed by a white unicorn |
| 10 | 0.024160136550546978 | 6746 | killed by a coyote |
| 11 | 0.036887590648350246 | 9791 | killed by a bat |
| 12 | 0.024160136550546978 | 4917 | killed by a bat |
| 13 | 0.17909953770432294 | 36762 | killed by a rabid rat |
| 14 | 0.11704996473565571 | 28988 | killed by a bolt of cold |

## What is the problem

The score is the mean of these games. 5 of 15 end at depth 1. The mean moves when a long game gets longer, and it falls when a long game gets shorter.

Watching the messages of the weak seeds (4, 8, 10, 11, 12) shows a second, quieter problem: the
wizard runs out of food. `You faint from lack of food` shows up repeatedly, and on seed 14 the
wizard starves to death next to corpses it never picks up. The pet makes it worse - the kitten
eats the jackal corpses the wizard kills. It is still not the biggest lever on the mean: of the
four variants tried this iteration, the ones that fed the weak seeds best (0.066) still lost more
on the long seeds than they gained, because every extra corpse in the pack costs arrange steps
and every corpse eaten costs 3-5 turns of standing still.

## What might solve it

See `experiments.md`. The short version: a corpse taints with age wherever it is, so there is no
pack-based larder, and the useful next levers are the pet stealing corpses and the dead spell
parser.