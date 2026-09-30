# Experiments on the brief

**Human-side log. Not the agent's.** The agent's memory is
`/workspace/experience.md` inside its own worktree; see `AGENTS.md`. This file
records one entry per *change to `loop/brief.py`*: what we predicted, why we
thought it, what the run did, and whether the prediction held.

**An experiment here must be able to fail.** A prediction that any outcome
would satisfy is not a prediction, and an entry whose outcome is "seemed fine"
has told us nothing. The cost is 9-153 minutes of CI per iteration (median 91),
which is the reason this loop is manual: automation would generate changes
nobody chose to make.

Verdict vocabulary, deliberately blunt:

- **keep** — the prediction held, or the change is right on mechanism alone
- **revert** — the prediction failed; the change is undone and the reason kept
- **inconclusive** — the run could not distinguish; do not count it either way

Read the numbers with `python meta/summarize.py`, and one run in full with
`python meta/summarize.py <run_id>`.

## E1 — tell the mutator not to revert its own work

**Change.** Added "Do not revert your own change" to `HOWTO`, and rewrote
`SCORING` to state the loop's real rule: the loop keeps anything that improves
the mean, however small; only a mean that went *down* discards it; only a `WIN`
needs the per-seed majority. Previously the brief demanded a per-seed bar for
keeping, which the harness did not.

**Prediction.** The mutator will stop discarding measured improvements, and
`reverted` in the run record will either disappear or come to mean "reverted a
regression".

**Why we thought it.** Run `36637347806` reverted a real `0.0624 → 0.0671`
improvement because the brief told it to. The rule was the bug, not the agent.

**Result.** `36710578461` reverted too — but measured `0.0430` against a
`0.0624` parent. Reverting that was right. The prediction is **kept but not
yet demonstrated**: the failure mode it targets (discarding a win) has not been
observed since, because no win has been measured privately and left in place.
See Open in `meta/experience.md`.

## E2 — make XP the stated objective

**Change.** Added `GOAL` (ascend; the score is a proxy) and replaced the depth
ladder in `SCORING` with the XP ladder, on the evidence that
`nethackers/arena/progress.py` scores `max(...)` and `Xp` wins on all 15 seeds.

**Prediction.** The mutator's hypotheses will stop being about depth, and more
of them will be about kills — since 73–97% of XP on this identity comes from
ordinary monsters the bot currently avoids.

**Why we thought it.** Both observed failures (`36615769123` climbing while
scoring 0.0374, and `36637347806` optimising depth) came from the agent
reconstructing a proxy because the real objective was not in the brief.

**Result.** Partly confirmed, and the second half is not yet. `36710578461`'s
hypothesis was "hunger, not kill rate, was capping the wizard's XP rate" — a
question about XP, not depth, and the right shape. But it tested the wrong half:
the agent spent its one experiment on turns rather than kills, and in a way
that cost it the XP gate. **Inconclusive** on the kill-rate prediction; the
framing change has not been falsified.

## E3 — `GAME_RULES.md` is the game, and nothing else

**Change.** `loop/build_game_rules.py` stopped emitting an objective, a depth
ladder, and per-bot verdicts ("must win at range or not at all", "reaches depths
the others never touch"). Added a `speed` column, verified against `monst.c`,
and made the build assert the alignment constants against `align.h`. The goal
moved into the brief.

**Prediction.** The mutator will read game facts and choose experiments from
them, rather than reasoning from a target the file used to supply.

**Why we thought it.** The file was mixing three different things — rules,
objectives, and judgements about our bot — and the judgements were the part
that went stale fastest.

**Result.** Not yet observable; this landed in the same commit as E1 and the
only run since, `36710578461`, was the first to see it. Its report cited
seed-level deaths and their causes, which is the shape we wanted, but one run
is not a result. **Inconclusive**, pending a run.

## E4 — `harvest_log` appends only what is new

**Change.** Rewrote `harvest_log` to match on entry headings and copy only
blocks the parent has not seen, and to drop the seeded placeholder. It was
appending the whole file, so every rejected mutant re-added all prior entries;
the old `new in existing` check compared a longer string against a shorter one
and could never fire.

**Prediction.** After several consecutive rejected turns, the parent's log
contains each entry exactly once.

**Result.** Confirmed by unit test, not by a run: three successive rejected
turns produce `e1`, `e2`, `e3` once each, and re-harvesting is a no-op.
**Keep.**

## E5 — publish every run's results

**Change.** `publish_results` pushes the surviving parent's `experience.md`,
`history.json` and any kept tree to `evolve-result/<identity>-<run_id>`. Not
registered to the hub, and not read by the next run.

**Prediction.** After any run, the findings and the log are recoverable
without digging in a 30-day transcript.

**Result.** Untested end to end — no run has completed on a commit containing
it. Unit-tested against a local bare remote: correct tree contents, idempotent
re-push, and a clean error record when the parent has no log. **Inconclusive**
until a run lands.

## E6 — does the experience log compose across iterations?

**Change.** None. This is a test of E1–E5 together, not a new brief.

**Prediction.** Over several iterations the log grows monotonically, later
hypotheses do not repeat earlier ones, and at least one iteration ends in a
`KEEP` — because the loop only learns from a kept tree, and three consecutive
`NOT-A-WIN`s with no keep would mean the loop is generating findings and no
progress.

**Result.** First attempt was abandoned before it could say anything, and the
reason is worth recording because it was not about the log.

Run `36728246238` was dispatched with `iterations=5` on the belief that an
iteration costs ~30-45 minutes. Eight successful single-iteration runs say
otherwise: 9, 42, 81, 87, 95, 96, 141, 153 minutes, median 91. Five iterations
need ~455 at the median, and a GitHub-hosted job is capped at 360 minutes with
no path to an exception. So the run could not have produced five iterations, and
because `Upload everything` and `Commit the verdict` sit *after* the loop in the
step order, a timeout would have left no artifact, no results branch and no
committed record at all. Cancelled at ~25 minutes rather than paying 4.5 hours
to learn that for certain. **Inconclusive** — and it says nothing about whether
the log composes.

Retargeted at 2-3 iterations, which is what fits. Note for whoever reads the
result: the `KEEP` prediction needs at least one kept tree, and two iterations
is a thin sample for "no hypothesis repeats". A negative here is weak evidence,
not a refutation.

## E7 — record the mutator's actual edit, not only its account of it

**Change.** `tree_diff` diffs each worktree against the parent it was seeded
from and writes `diff-<n>.patch`, plus a complete per-file stat in
`history.json`. The patch reaches the results branch under `diffs/`. Harness
files and binaries are excluded. The brief no longer says a kept tree "is not
published", which stopped being true when E5 landed — it now says *not
registered with the leaderboard*, which is the distinction the sentence was
actually for.

**Prediction.** For any future rejected mutant, the code it wrote is readable
without the artifact transcript. No effect on verdicts.

**Result.** Confirmed locally, and the motivation is a defect rather than a
preference: the brief repeated "9 of 13 killers have mmove 12 (max speed)" —
false, and taken from the discarded tree of run `36637347806`. The agent said
it had fixed starvation and it could not be checked, because a binned tree left
only the agent's prose. The stat/patch split keeps the complete file list even
when the patch is capped, so a truncated record degrades to "read less", not
"cannot tell what was touched". Verified end to end against a local remote: two
rejected iterations' patches both present, a zero-byte patch correctly
dropped.

This does not make the agent trustworthy — a patch bounds how long an
unverifiable claim survives, it does not prevent one. A later run should check
whether a reported fix matches the recorded diff.

## E8 — cost: the brief was silently deleting the harness's own instructions

**Question.** Why did one iteration take 95.4 minutes (run 36710578461) when
the score it produced needed ~13?

**Answer. Measured, not guessed.** 1.0 min setup, 6.4 min baseline score,
81.3 min in the agent, 0.1 min smoke, 6.5 min child score. Of the agent's 81.3
minutes, 56.0 were `sleep` — 25 unique waits including `sleep 600` and
`sleep 420`. It had written `/tmp/eval.sh`, launched it backgrounded at PAR=4/5,
and then blocked on it. So each seed was played two or three times per
iteration: the agent's own batch, our parent baseline, our child score.

Three separate causes, which is why the fix is three commits' worth:

1. **We removed the measurement instructions.** `build_brief` has no free-text
   parameter, so `ContainerOperator.run(brief=...)` *replaces* the harness
   brief rather than extending it. Upstream ends with `HOWTO, MEASURE`; every
   brief this loop composed therefore silently lost `MEASURE`, and with it the
   canonical `arena.run` invocation, the `--evaluation-id` namespace, and the
   "one foreground command, do not background or sleep" rule. The agent was
   not misbehaving — it had never been told.
2. **Serial scoring was free to fix.** `score()` pinned
   `max_parallel_evals=1`: ~6.4 min per score, ~13 min per iteration. It bought
   nothing. `run_prepared` keys results by spec index after `as_completed` and
   returns them in `specs` order, so the worker count cannot reach the result.
3. **No bound on a turn.** One confused agent could spend a 360-minute job.

**Fixed** in `2cb0dd1`: import `MEASURE` from the package rather than retyping
it (it cannot drift the way ours did), cap the agent's own check at 5 seeds
because the harness re-scores all 15 anyway, parallelise scoring 4-wide, and
bound a turn at 40 minutes through the operator's own `stop` event.

**What this says about the brief generally.** The brief is the mutator's only
instruction channel, so a missing section is not a smaller prompt, it is a
wrong one. The three bugs that cost this loop the most — no `MEASURE`, and
earlier an empty first brief — were all omissions, not bad wording. When a
custom brief replaces a curated one, the first question is not "is mine
better?" but "what did theirs say that mine does not?"

**Not claimed.** No timing is updated from an estimate. The fix lands as
`2cb0dd1` and the first run on it is the measurement; if the agent still
sleeps, E8 has located the cost without having removed it.

## E9 — GAME_RULES.md was carrying measurements while claiming not to

**Question.** The open list said `GAME_RULES.md` "still carries a measured
killer/death table with seed counts. That is empirical, not game-mechanical."
What is the right scope for a file that is inlined into the agent's prompt?

**Answer. The file should be a pure function of the identity and the source
tag.** It was taking a `diagnosis.json` and listing the creatures that had
actually killed a seed, with a per-creature seed count, under a heading that
read "What killed this bot". Two things were wrong, and the second is why this
was not just tidied up:

1. It contradicted its own header, which says the file "contains no objective
   and no scoring" and is "the game only".
2. Those counts are 15 published seeds — **not the seeds the leaderboard scores
   on**. Telling the agent "wolf killed 2 of your seeds, go and handle wolves"
   is exactly the overfit the rest of the loop is built to prevent, delivered
   through the one channel the agent trusts. It is the same failure as the
   `9 of 13 killers have mmove 12` line that run `36637347806` propagated from a
   discarded tree: an unverifiable number that reads like documentation.

**Change.** The generator now takes `(identity, out.md)` — no measurement input
at all — and scope is chosen mechanically: every creature in `monst.c` at level
≤ `LEVEL_BAND` (2), i.e. 52 creatures, the band a starting character meets.
"Because it contains no results" is now structural rather than a promise; there
is nothing to leak in. The seed counts, the "died to" column and the
death-framed heading are gone, replaced by source-derived facts the agent can
use without having seen a single seed.

The rewrite is also a better file. `killer bee` is AC 5 at weight 1 — the
hardest creature in the band is also one of the smallest, which is a fact about
the game and a far more useful thing to reason about than which creature
happened to be common. REGEN on the lycanthropes, FLY on the six fliers, speed 0
on the four molds, and the damage types that armour does not stop are all now
stated as mechanics rather than as things that happened.

**The dangling footer, separately.** The file ended by telling the agent to
"regenerate with `python loop/build_game_rules.py <identity>
<diagnosis.json> GAME_RULES.md`". The agent cannot do this: `GAME_RULES.md` is
inlined into the brief by `game_rules_section()`, and the worktree is a copy of
the bot tree containing only `bot.py` and `autoascend/`. There is no `loop/`
directory in that container. This is the same class of defect as the `/refs/`
reference that `MEASURE` used to carry, and it arrived by a different route —
through *generated* text, which nobody reviewed as prompt. Generated files that
get inlined are prompt, and have to be held to the same rule as hand-written
ones. The instruction now lives in the generator's docstring and `AGENTS.md`.

**What this says.** Two of the three prompt defects this loop has suffered from
were omissions (no `MEASURE`, an empty first brief) and one was an inclusion
(measurements in a facts file). All three were invisible because the brief is
assembled from parts written at different times by different hands — one of them
a generator. "Is this section still true?" is worth asking of the generated
pieces too.

**Cost.** The brief grew from 22.3 KB to 26.9 KB, since 52 creatures is more
table than 14 death-derived rows. That is paid for in prompt length, and it is
not yet clear it is worth it; the first run to measure it will also be the first
to show whether the agent uses the wider band.

## Open

- E6 is the only unsettled experiment, and it is waiting on a run rather than a
  decision.
- E8 is implemented but unmeasured. The expected saving is ~13 min of scoring
  plus most of the agent's 56 min of sleeping, which would put an iteration
  near 30 min and make five fit the ceiling — but that is arithmetic, not
  evidence, and it must not be written down as a result until a run on
  `2cb0dd1` reports it.
- The loop has no checkpoint. A timeout costs every iteration in the job, not
  the one in flight, because `publish_results` runs only at the end. Calling it
  per iteration would make the results branch the checkpoint for the cost of one
  function call, and would leave "iterations" a request about progress rather
  than a bet on the clock. Deferred: the 360-minute ceiling makes 2-3
  survivable, not comfortable.
- CI minutes are the real constraint on this whole loop. At a median 91 minutes
  an iteration and a 2,000/month free-tier budget, we get roughly 20 iterations a
  month. That, not the agent's ideas, is what limits how much the brief can be
  tested.
- Nothing has ever been kept over five iterations, so the loop has no evidence
  yet that it can compose improvements rather than only accumulate findings.
