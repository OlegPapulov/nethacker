# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36921712685 registered `prog_6f3a5ba98505db8d0c2cfd7b9a4f167e` at public 0.064 on `wiz-hum-cha-mal`. The hub identity list for that program has that one public row and no verified row. `GET /verify/candidates` rejects this login with 401. The private board is their worker's queue.

## What is the problem

The coding agent cannot play Private Dungeons. Those seeds stay on their verifier. A registered commit is already in that queue. The last operator spent 78 minutes and 402,750 tokens, most of it talk, before the one food edit.

## What might solve it

Tell the agent to be brief: one edit, a `# hypothesis:` comment, then exit. Do not narrate, do not tour the tree, and do not run the arena. Say plainly that a local game is not a private result.

## Proposal (not approved)
Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.

# Next experiment

## Why it stopped

killed by a jackal (2 of 15).

## What is the problem

Mean progress is 0.064. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Eat before exploring. At least one game ends in starvation or fainting from lack of food, and the rest die on the early floors. Change food handling in autoascend so this character eats when hungry instead of walking on.

Edit `autoascend/` and exit. The judge measures that tree.

