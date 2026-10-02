# Mutator runs

## Run wiz-hum-cha-mal, 10-minute cap, 3 iterations

The parent batch mean was 0.062. Nine of 15 games end at depth 1. One official death is starvation (seed 13). The written experiment told the agent the usual stop was "killed by a wolf" (2 games) and to change melee.

### Why it stopped

All three iterations exited 137. That is the 10-minute `docker kill`. The agent was still in tool calls or reasoning. No edit was scored (`dev_fitness` empty). The log recorded each iteration twice.

### What is the problem

The cap is doing what it was set to do, and the prompt spends that window re-playing seeds the notes already list. On the last iteration the model had found seed 3 fainting from lack of food and seed 13 starving, and it was about to write its own eval harness when it was killed.

### What might solve it

The notes must forbid another arena run, and a starvation or fainting death must become the experiment even when a monster name is more common. The run log must keep a short reason, not the model's transcript.

## Run 36861664309, wiz-hum-cha-mal, 10-minute cap, 3 iterations

[36861664309](https://github.com/OlegPapulov/nethacker/actions/runs/36861664309) finished with the job green and `0/3` elites. Cold-start mean was 0.062 (the table printed 0.063). Nine of 15 games end at depth 1. The modal death is a wolf (seeds 4 and 11). Seed 13 dies of starvation at 5,206 turns on depth 1. Seed 3 dies to a grid bug at 3,052 turns.

The seed notes already said to eat before exploring and not to re-play the seeds. The agent never rewrote them (`notes_ignored` true).

### Why it stopped

Each coding container was killed at the 10-minute cap. Wall times inside `evolve`: iteration 1 at 819s (~601s of thinking), iteration 2 at 1436s (~615s), iteration 3 at 2052s (~614s). Exit 137, then `aborting — 3 consecutive operator failures`. `dev_fitness` is empty on all three. The only event left in the Actions log is an OpenCode `step_start`. No tool result, no diff, no score.

### What is the problem

The default reasoning variant of `opencode/big-pickle` does not finish one edit inside 10 minutes. The Actions log no longer shows a diagnosis transcript, because the kill lands before a step completes. A longer transcript would not help: the iteration is discarded either way.

### What might solve it

Pass `--effort medium` (OpenCode applies that as `--variant medium` on the pinned model) and kill the container at 20 minutes. The bot experiment stays "eat before exploring."

## Run 36867649207, wiz-hum-cha-mal, 20-minute cap, `--effort medium`

[36867649207](https://github.com/OlegPapulov/nethacker/actions/runs/36867649207) finished green with `0/3` elites. Cold-start mean was 0.062. The published log records three operator errors and no `dev_fitness`.

| Iteration | Thinking time | Last event | Measured |
|---|---|---|---|
| 1 | ~1209s | `step_start`, exit 137 | no |
| 2 | ~1216s | `step_start`, exit 137 | no |
| 3 | ~1216s | `step_start`, exit 137 | no |

`evolve` then aborted on 3 consecutive operator failures.

### Why it stopped

The 20-minute `docker kill` is exit 137. In `nethackers` that path records `operator-error` and never calls the judge. A file the agent wrote inside the container is not a measured bot. The Actions log for this run does not contain a scored iteration.

### What is the problem

The seed header told the agent not to run the arena, and that an unchanged note file discards the edit. The harness brief says the opposite: edit `autoascend/` with a `# hypothesis:` comment, and the judge re-scores the tree after the process exits. Killing the process skips that measurement. Raising the cap from 10 minutes to 20 did not produce a score.

### What might solve it

Stop killing the coding container. Point the seed notes at `experiments.md` and tell the agent to edit `autoascend/` and exit, so the judge can measure the tree.

## Run 36881136099, wiz-hum-cha-mal, no host kill

[36881136099](https://github.com/OlegPapulov/nethacker/actions/runs/36881136099) played all three iterations and the job exited 1. Cold-start mean was 0.063. Each child beat its parent on the 15 public seeds. None of them were published.

| Iteration | Operator | Tokens | Judge mean | Hub |
|---|---|---|---|---|
| 1 | 96 min, completed | 703557 | 0.078 | local-only |
| 2 | 78 min, completed | 679463 | 0.079 | local-only |
| 3 | 85 min, completed | 618055 | 0.081 | local-only |

The judge table for iteration 3 prints 0.082. Seed 13, the starvation game, went from 5,206 turns at depth 1 to 24,520 turns at depth 4. The notes were not rewritten (`notes_ignored` true). The code change was scored anyway.

### Why it stopped

`nethackers` reported `local-only: not published (no gh publisher / dev owner)` on every iteration. `mutator/loop.py` returns 1 when that field is set, so the Actions step is red. The log line `✓ improved 1 cell(s) dev=0.081 (kept local)` is the same fact: the tree beat the parent and stayed on the runner.

### What is the problem

`gh` was logged in. The preflight `GET /user` and the push check both passed. Publish then clones `OlegPapulov/nethacker` into a fresh temp directory and commits there. The job sets `user.name` and `user.email` only on the checkout, so that clone has no author. `git commit` fails, `nethackers` swallows the error, and the hub never sees the tree. The runner is deleted with the 0.081 bot still only in that workspace. The next checkout of `main` is the 0.062 baseline again.

### What might solve it

Set the git author globally in the mutate job, so the publish clone can commit and push. Commit the improved bot from the runner workspace onto `main` as well, so the next run starts from the scored tree if the hub push fails.

## Run 36921712685, wiz-hum-cha-mal, 1 iteration

[36921712685](https://github.com/OlegPapulov/nethacker/actions/runs/36921712685) finished green. Cold-start mean 0.063. One iteration, 78 minutes, 402,750 tokens, then `✓ REGISTERED dev=0.064`. `hub_reason` is empty. The published tree is `ea143fc` on `evo-harness-v1/20261001-203217`.

The edit is the starvation experiment. When hunger reaches weak, the wizard walks to a corpse and eats it. A corpse it is already standing on is treated as fresh. Seed 13 went from starvation at 5,206 turns on depth 1 to 31,848 turns on depth 3 (0.024 to 0.075). Seed 4 went the other way: 32,346 turns on depth 7 (0.179) down to 2,644 turns on depth 1 (0.018). Seed 11 fell from 0.117 to 0.037. The mean moved from 0.063 to 0.064.

### Why it stopped

The job succeeded. The record commit on `main` (`3d6aba1`) contains only `experience.md` and `experiments.md`. The next checkout is still the 0.062 baseline.

### What is the problem

`nethackers` writes the iteration at `runs/<id>/work/iter-0`. `mutator/loop.py` looked for `runs/<id>/iter-0`, found nothing, and did not copy the tree into the checkout. `notes_ignored` is true for the same reason. The hub has the bot. `main` does not.

### What might solve it

Look for `runs/*/work/iter-*`, and copy those two AutoAscend files from `ea143fc` onto `main` so the next seed is the registered bot.

The hub program is `prog_6f3a5ba98505db8d0c2cfd7b9a4f167e`. Its identity list is the one public row at 0.064. There is no verified row, so Private Dungeons has not scored it. This login cannot read `/verify/candidates` (401). Their verifier is the only process that writes that board.

## Run wiz-hum-cha-mal (2 iteration(s))
- iteration 1: reason=no-cell-improved dev_fitness=0.06346935845057744 improved=False notes_ignored=True
- iteration 2: reason=no-cell-improved dev_fitness=0.060242576435499684 improved=False notes_ignored=True

### Why it stopped
no-cell-improved

### What is the problem
# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

2 of 15 games stopped at killed by a jackal. Mean progress 0.064.

| seed | progress | turns | stop |
| --- | --- | --- | --- |
| 0 | 0.07453595273884014 | 27740 | killed by an ape |
| 1 | 0.11704996473565571 | 21697 | killed by a fire ant |
| 2 | 0.07453595273884014 | 24862 | killed by Ms. Melac; the shopkeeper |
| 3 | 0.07453595273884014 | 19861 | killed by an invisible gnome king |
| 4 | 0.01847840456172601 | 2644 | killed by a kobold zombie |
| 5 | 0.036887590648350246 | 8788 | killed by a sewer rat |
| 6 | 0.11704996473565571 | 27730 | killed by a lynx |
| 7 | 0.11704996473565571 | 34603 | killed by a rope golem |
| 8 | 0.02081163581974355 | 4142 | killed by a giant rat |
| 9 | 0.07453595273884014 | 25313 | killed by a jackal |
| 10 | 0.07453595273884014 | 29898 | killed by a lizard |
| 11 | 0.036887590648350246 | 12486 | killed by a jackal |
| 12 | 0.024160136550546978 | 4917 | killed by a bat |
| 13 | 0.07453595273884014 | 31848 | killed by a white unicorn |
| 14 | 0.029108986017138745 | 7795 | died of starvation |

## What is the problem

The score is the mean of these games. 6 of 15 end at depth 1. A change that does not move the usual stop, killed by a jackal, does not change the mean.

## What might solve it

See `experiments.md`.

### What might solve it
See the proposal in experiments.md. Do not edit mutator/ until a human approves it.

