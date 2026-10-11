# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit. This note does not state a death, so no specific end is described here. What the code establishes is that no seed ever reached experience level 12 while staying on the first dungeon level: the mean of 0.114 means the runs bank their highest experience level somewhere between level 8 and level 11 and end there. The run ends before the farm floor delivers the kills that would push past that.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches. The experience level is the milestone that moves this score, and the games die before the farm reaches level 12.

## What might solve it

The runs end while still farming the first Doom levels. The parent's fight logic ignores every monster farther than 7 BFS squares, so on the farm floor it leaves approaching monsters unfought; those kills are the lost experience and the lost fresh corpses. Engaging those monsters out to 12 squares, while on the farm floors and healthy, banks more levels before the end. See `experiments.md`.
