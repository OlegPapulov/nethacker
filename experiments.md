# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36867649207: three exits 137 at about 20 minutes. `dev_fitness` is empty. `evolve` aborted after three operator failures and registered nothing.

## What is the problem

`nethackers` measures a tree only after the operator process exits. `docker kill` makes that exit 137, which is recorded as an operator error and is not scored. The seed header also fought the harness brief: it forbade another arena run and said an unchanged note file discards the edit. The harness brief already tells the agent to change `autoascend/` and then waits for a clean exit before it measures.

## What might solve it

Remove the host kill. The container keeps nethackers' own 8-hour ceiling, and the Actions job still stops at 360 minutes. Rewrite the seed header so it names the change in `experiments.md`, asks for that edit in `autoascend/` with a `# hypothesis:` comment, and tells the agent to exit so the judge can score.

## Proposal (not approved)
Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.

# Next experiment

## Why it stopped

killed by a wolf (2 of 15).

## What is the problem

Mean progress is 0.062. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Eat before exploring. At least one game ends in starvation or fainting from lack of food, and the rest die on the early floors. Change food handling in autoascend so this character eats when hungry instead of walking on.

Edit `autoascend/` and exit. The judge measures that tree.

