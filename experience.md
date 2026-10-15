# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The batch is the parent run recorded in `/refs/parent-eval.json`, one game per
seed (15 seeds). The bot farms the first Doom level to experience level 12 and
almost never gets there. The games end as follows:

- Xp2, depth 2: killed by a goblin.
- Xp4, depth 2: killed by a kitten.
- Xp5, depth 2: killed by a kobold lord.
- Xp8, depth 1: killed by a bolt of fire.
- Xp8, depth 4: killed by a pony.
- Xp8, depth 1: killed by a bolt of cold.
- Xp9, depth 1: killed by a shattered potion.
- Xp10, depth 1: killed by a rothe.
- Xp10, depth 3: poisoned by a rotted rothe corpse.
- Xp10, depth 5: killed by a dwarf lord.
- Xp11, depth 1: killed by a dwarf lord.
- Xp11, depth 1: killed by a fire ant.
- Xp11, depth 1: killed by a soldier ant.
- Xp11, depth 1: killed by a soldier ant.
- Xp11, depth 3: killed by an invisible Mordor orc.

## What is the problem

Most games die in melee at experience level 10 or 11, the last stretch before the
level-12 gate that ends the farm. The wizard walks up to a heavy hitter it cannot
out-damage and trades blows until it dies: a soldier ant or fire ant (four games),
a dwarf lord (two), a rothe and a Mordor orc. The other half of the batch is traps
(a bolt of fire, a bolt of cold), poison from a rotted rothe corpse, a shattered
potion, and three very early deaths on depth 2 to a goblin, kitten, and kobold lord.

The common shape: the hurt wizard keeps approaching a dangerous slow monster. A
soldier ant and a fire ant are already on the dangerous list, and a dwarf lord, a
rothe, and an orc are not.

## What might solve it

See `experiments.md`.
