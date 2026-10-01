# Mutator runs

## Run wiz-hum-cha-mal, 10-minute cap, 3 iterations

The parent batch mean was 0.062. Nine of 15 games end at depth 1. One official death is starvation (seed 13). The written experiment told the agent the usual stop was "killed by a wolf" (2 games) and to change melee.

### Why it stopped

All three iterations exited 137. That is the 10-minute `docker kill`. The agent was still in tool calls or reasoning. No edit was scored (`dev_fitness` empty). The log recorded each iteration twice.

### What is the problem

The cap is doing what it was set to do, and the prompt spends that window re-playing seeds the notes already list. On the last iteration the model had found seed 3 fainting from lack of food and seed 13 starving, and it was about to write its own eval harness when it was killed.

### What might solve it

The notes must forbid another arena run, and a starvation or fainting death must become the experiment even when a monster name is more common. The run log must keep a short reason, not the model's transcript.
