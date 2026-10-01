# Mutator runs

## Run wiz-hum-cha-mal, 10-minute cap, 3 iterations

The parent batch mean was 0.062. Nine of 15 games end at depth 1. One official death is starvation (seed 13). The written experiment told the agent the usual stop was "killed by a wolf" (2 games) and to change melee.

### Why it stopped

All three iterations exited 137. That is the 10-minute `docker kill`. The agent was still in tool calls or reasoning. No edit was scored (`dev_fitness` empty). The log recorded each iteration twice.

### What is the problem

The cap is doing what it was set to do, and the prompt spends that window re-playing seeds the notes already list. On the last iteration the model had found seed 3 fainting from lack of food and seed 13 starving, and it was about to write its own eval harness when it was killed.

### What might solve it

The notes must forbid another arena run, and a starvation or fainting death must become the experiment even when a monster name is more common. The run log must keep a short reason, not the model's transcript.

## Run wiz-hum-cha-mal (3 iteration(s))
- iteration 1: reason=operator-error:opencode2 operator exited with status 137: {"type":"step_start","timestamp":1790858284179,"sessionID":"ses_f088b0a37ffeHHlvzCgOr7eA02","part":{"id":"prt_0f778cc91001… dev_fitness=None improved=False notes_ignored=True
- iteration 2: reason=operator-error:opencode2 operator exited with status 137: {"type":"step_start","timestamp":1790859206703,"sessionID":"ses_f0881da4cffenlWm19h4rAbj6p","part":{"id":"prt_0f786e02d001… dev_fitness=None improved=False notes_ignored=True
- iteration 3: reason=operator-error:opencode2 operator exited with status 137: {"type":"step_start","timestamp":1790859796571,"sessionID":"ses_f08786ee8ffe1Bv6YHk65IbhOw","part":{"id":"prt_0f78fe057001… dev_fitness=None improved=False notes_ignored=True

### Why it stopped
operator-error:opencode2 operator exited with status 137: {"type":"step_start","timestamp":1790859796571,"sessionID":"ses_f08786ee8ffe1Bv6YHk65IbhOw","part":{"id":"prt_0f78fe057001nMYbPSvT6Dmdkw","messageID":"msg_0f78fcc7300165yNBZm56NbpYm","sessionID":"ses_f08786ee8ffe1Bv6YHk65IbhOw","type":"step-start"}}

### What is the problem
# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

2 of 15 games stopped at killed by a wolf. Mean progress 0.062.

| seed | progress | turns | stop |
| --- | --- | --- | --- |
| 0 | 0.036887590648350246 | 13697 | killed by a goblin |
| 1 | 0.036887590648350246 | 17693 | killed by a jackal |
| 2 | 0.07453595273884014 | 20700 | killed by a white unicorn |
| 3 | 0.02081163581974355 | 3052 | killed by a grid bug |
| 4 | 0.17909953770432294 | 32346 | killed by a wolf |
| 5 | 0.0507583712345433 | 14486 | killed by a bat |
| 6 | 0.036887590648350246 | 11919 | killed by a kitten |
| 7 | 0.07453595273884014 | 23971 | killed by a rothe |
| 8 | 0.07453595273884014 | 23604 | killed by a soldier ant |
| 9 | 0.07453595273884014 | 24295 | killed by an ape |
| 10 | 0.024160136550546978 | 4014 | killed by a hobbit |
| 11 | 0.11704996473565571 | 27094 | killed by a wolf |
| 12 | 0.036887590648350246 | 12509 | killed by a newt |
| 13 | 0.024160136550546978 | 5206 | died of starvation |
| 14 | 0.07453595273884014 | 22485 | killed by a crossbow bolt |

## What is the problem

The score is the mean of these games. 9 of 15 end at depth 1. A change that does not move the usual stop, killed by a wolf, does not change the mean.

## What might solve it

See `experiments.md`.

### What might solve it
See the proposal in experiments.md. Do not edit mutator/ until a human approves it.

