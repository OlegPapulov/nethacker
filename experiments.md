# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36861664309: three operator exits 137. Each container lived about 10 minutes and the last event was an OpenCode `step_start`. No edit was scored.

## What is the problem

`opencode/big-pickle` is pinned with no `--effort`, so OpenCode uses its default reasoning variant. That variant does not land a diff before the 10-minute `docker kill`. The seed notes already named starvation and forbade another arena run.

## What might solve it

Call `nethackers evolve` with `--effort medium`. nethackers 0.37.3 turns that into `opencode2 run --variant medium` beside `--model opencode/big-pickle`. Raise the host kill from 600s to 1200s, and tell the agent the container dies at 20 minutes.

## Proposal (not approved)
Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.

# Next experiment

## Why it stopped

killed by a wolf (2 of 15).

## What is the problem

Mean progress is 0.062. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Eat before exploring. At least one game ends in starvation or fainting from lack of food, and the rest die on the early floors. Change food handling in autoascend so this character eats when hungry instead of walking on. Do not re-run the seeds.

Do not run Python against the game. Edit `autoascend/` only.

