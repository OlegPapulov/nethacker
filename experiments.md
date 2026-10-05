# Next mutator experiment

Not applied. The operator brief is rewritten locally. No run is dispatched.

## Why it stopped

Run 37372752441 scored 0.10051000771701067. The parent is 0.11444300565928403. The mean falls by 0.014.

## What is the problem

The operator brief still asks for one idea that raises the score. The operator then writes a new path. This time the path keeps a wizard below level 6 on dungeon level 1. The mean falls.

## What might solve it

The brief has one job. Develop a bot for NetHack 3.6.6. Read `GAME_RULES.md`. Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. The identity is `wiz-hum-cha-mal`. Describe the games in `experience.md`. Propose the change in `experiments.md`. Change the bot from that proposal.

## Result

- iteration 1: 0.101 not kept (no-cell-improved). Decreases the mean by 0.014 (from 0.114 to 0.101).
