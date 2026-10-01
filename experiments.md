# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36861664309: three operator exits 137. Each container lived about 10 minutes and the last event was an OpenCode `step_start`. No edit was scored.

## What is the problem

`opencode/big-pickle` is pinned with no `--effort`, so OpenCode uses its default reasoning variant. That variant does not land a diff before the 10-minute `docker kill`. The seed notes already named starvation and forbade another arena run.

## What might solve it

Call `nethackers evolve` with `--effort medium`. nethackers 0.37.3 turns that into `opencode2 run --variant medium` beside `--model opencode/big-pickle`. Raise the host kill from 600s to 1200s, and tell the agent the container dies at 20 minutes.
