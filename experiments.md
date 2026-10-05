# Next mutator experiment

Applied. The seed, the rulebook, and the brief now state one score rule and one edit.

## Why it stopped

Run 37286220190 scored 0.11444300565928403. That is the parent score. The mean turn count is 36,648 on both tables.

## What is the problem

The operator read two jobs. The brief said one idea, any amount of code, and a live game. The seed said one uncomment and no local game. The rulebook said every other file matches the parent and did not name `agent.py`.

The commented Elbereth block is a bad uncomment. It rests for 8 turns. `emergency_strategy` preempts `fight2`.

## What might solve it

The score is the mean of the 15 judge seeds. A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean.

The edit is one engrave of Elbereth in `emergency_strategy`. The rest loop stays commented. Do not call `direction('.')`. The file that may change is `agent.py`.

## Result

- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). The Elbereth block stays commented. The bot files match the parent.
