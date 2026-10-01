# Next mutator experiment

Applied with this change.

## Why it stopped

Exit 137 at 10 minutes, three times, before any scored edit.

## What is the problem

`experience.md` already had the 15 deaths. The agent treated that as a starting point for its own diagnosis, including a new eval harness. The hypothesis picker named "killed by a wolf" because that string occurred twice, and ignored the one starvation.

## What might solve it

Tell the agent the table is final and that the container dies at 10 minutes. If any death mentions starvation, hunger, or fainting, that is the experiment. Dedupe the metric rows and truncate the recorded reason.
