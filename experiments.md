# Next mutator experiment

Applied with this change.

## Why it stopped

Exit 137 at 10 minutes, three times, before any scored edit.

## What is the problem

`experience.md` already had the 15 deaths. The agent treated that as a starting point for its own diagnosis, including a new eval harness. The hypothesis picker named "killed by a wolf" because that string occurred twice, and ignored the one starvation.

## What might solve it

Tell the agent the table is final and that the container dies at 10 minutes. If any death mentions starvation, hunger, or fainting, that is the experiment. Dedupe the metric rows and truncate the recorded reason.

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

