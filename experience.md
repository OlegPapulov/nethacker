# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

Every game in the parent batch ends in death on the first floors. Ten of the
fifteen seeds never leave dungeon level 1, and the deepest any seed reaches is
level 5. The ends are, per seed:

- seed 0: killed by a rothe (Xp:10, dlvl 1)
- seed 1: killed by a dwarf lord (Xp:11, dlvl 1)
- seed 2: killed by a bolt of fire (Xp:8, dlvl 1)
- seed 3: killed by a fire ant (Xp:11, dlvl 1)
- seed 4: killed by a goblin (Xp:2, dlvl 2)
- seed 5: killed by a soldier ant (Xp:11, dlvl 1)
- seed 6: killed by a soldier ant (Xp:11, dlvl 1)
- seed 7: poisoned by a rotted rothe corpse (Xp:10, dlvl 3)
- seed 8: killed by a shattered potion (Xp:9, dlvl 1)
- seed 9: killed by an invisible Mordor orc (Xp:11, dlvl 3)
- seed 10: killed by a kitten (Xp:4, dlvl 2)
- seed 11: killed by a pony (Xp:8, dlvl 4)
- seed 12: killed by a kobold lord (Xp:5, dlvl 2)
- seed 13: killed by a dwarf lord (Xp:10, dlvl 5)
- seed 14: killed by a bolt of cold (Xp:8, dlvl 1)

Ten of the fifteen are melee kills (rothe, dwarf lord, fire ant, soldier ant,
soldier ant, invisible Mordor orc, kitten, pony, kobold lord, dwarf lord). Two
are the bolt trap the rules call out -- fire (2) and cold (14). One is the rotten
corpse the rules call out (7). The rest are early mishaps (a goblin, a shattered
potion).

## What is the problem

The score is the mean of the fifteen seeds, and progress is the highest milestone a
game reaches. The milestones here are Xp:11 (seeds 1, 3, 5, 6, 9), Xp:10 (0, 7,
13), Xp:8 (2, 11, 14), Xp:5 (12), Xp:4 (10), Xp:2 (4) -- mean 0.1482. The clauses
that would move that mean are Xp:11 (0.2548) and Xp:12 (0.3326): the parent holds
five games one step short of Xp:12, and that single step is worth +0.078 on a seed.
No seed ever banks it.

The bot is told to stay on dungeon level 1 and farm experience until level 12, and
the farm is a race between experience and food/time. It spends tens of thousands of
turns (56k-92k) on the floor, much of it walking to corpses or fainting, and the
character has no usable ranged attack for most of that time. It reaches level 10-11
and then a monster that has spawned on the floor reaches melee range and kills it
before it finishes the last level or two. The turns spent reaching corpses are
turns not spent gaining experience, so anything that lets the wizard take more
actions -- or more kills -- per unit of food is directly on the critical path to
Xp:12.

## What might solve it

See `experiments.md`.
