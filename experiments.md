# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36881136099 scored three improvements, 0.063 to 0.078 to 0.079 to 0.081, and published none of them. The job exited 1 on `hub_reason`.

## What is the problem

The publish clone is a new git repo. Author identity set with `git config` on the Actions checkout does not apply there, so `git commit` fails and `nethackers` records the win as local-only. The record step on `main` saves only `experience.md` and `experiments.md`, so the scored tree is discarded with the runner.

## What might solve it

Set `user.name` and `user.email` with `git config --global` before `nethackers evolve`. In the record step, also commit `bot.py`, `arena_adapter.py`, `autoascend/`, `nethackers.solution.json`, and `LICENSE` when the loop left an improved tree in the workspace.
