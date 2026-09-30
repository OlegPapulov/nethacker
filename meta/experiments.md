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

**Result.** **Failed in CI, for a reason no local test could have caught.**

`36731664027` (old SHA `1cd8a82`) ran to completion — 2 iterations, 4h 00m 41s —
and published nothing:

```
results NOT published (push failed: git push failed (128):
  fatal: could not read Username for 'https://github.com': No such device or address)
```

`publish_results` stages into a directory it creates with `git init`.
`actions/checkout` persists the job's token as an
`http.https://github.com/.extraheader` entry in the **checkout's** local config,
and a repository created by `git init` does not inherit another repository's
config. The staging repo therefore had no credential at all. Note what that
error is *not*: it is not a 403, and not a permissions problem. It is git
finding nothing to offer and falling back to an interactive prompt, on a runner
with no terminal. The unit test against a local bare remote passed because a
developer's machine has a credential helper in *global* config, which every repo
does read — the bug is only invisible from a laptop.

Fixed by `_push_auth`, which reads the header out of the repo that has it and
passes it with `-c` on the push. No second token, and scoped to the repo being
pushed to. Returns `[]` when there is no header, so local behaviour is unchanged.
Verified by reproducing the original condition (a fresh repo seeing
`NOTHING`) and by a full `publish_results` against a local remote.

The deeper lesson is recorded as E10: the artifact fallback was a claim, not a
fact, and it was false.

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

**Second attempt, `36731664027`: the `KEEP` prediction held, on the first
measured test of it.**

| it. | verdict | child | parent | forward/back |
|---|---|---|---|---|
| 1 | `NOT-A-WIN` | 0.06245 | 0.06242 | 5 / 7 |
| 2 | **`KEEP`** | **0.06612** | 0.06242 | 8 / 7 |

This is the first kept tree the project has produced, and it is the first time
the loop has advanced its own parent. Iteration 2 also behaved the way the log
mechanism is supposed to: it read iteration 1's harvested findings, noticed that
iteration 1 had repaired `cast()` for diagonal targets, and did not go near
casting — its hypothesis was about search decay instead. 60 scratch files in its
own worktree, one real change: `search_count ** 2 * 2` → `* 8`.

The `KEEP` is honest about its own weakness, and so should this record be. 8
forward against 7 backward clears "not a regression" and misses the two-thirds
bar; +0.0037 is well inside the 0.0109 SE. The agent validated on 15 held-out
trajectory ids (0.0407 → 0.0522) and reported a non-monotonic coefficient curve
(2→.0624, 4→.0548, 8→.0661, 16→.0553, none→.0243), which is what noise looks
like. **The loop kept a direction, not a proven win.** The kept tree is the best
bot this project has had and it is not a leaderboard entry.

Still thin on "no hypothesis repeats" — two iterations. And the run cost 120
minutes per iteration, the slow end of the observed range, so E8's savings
remain unmeasured on top of this.

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

**First CI run of `tree_diff`, `36731664027`: it works, and it was very nearly
useless anyway.**

`history.json` carried both iterations' complete per-file stats, so the stat
half held up. The patch half did not reach anyone: both `diff-001.patch` and
`diff-002.patch` were written to `runs/`, and the artifact upload list did not
include `runs/diff-*.patch`. Neither did the kept tree, nor the run record, nor
the results staging directory. See E10.

What the surviving `history.json` does show is the failure mode the exclusion
list was built for, arriving in a form it does not cover. Iteration 2 touched
**61 files**, 60 of them agent scratch under `.tmpwork/` — instrumented copies
of `agent.py`, 30 result JSONs, diagnostic scripts. The one real edit,
`autoascend/exploration_logic.py +11/-1`, was the *last* entry and was 4 lines
from the truncation cut. Iteration 1 did the same thing at the repository root,
leaving `direct_run.py` and `local_eval.py` in the tree.

So the recorder is faithful — those files really were added — and the record is
still close to unreadable, and worse, those scratch files are now *inside the
kept tree* and will be carried into every future parent and shipped to the hub.
Excluding `experience.md` and `brief-*.md` did not help because the problem was
never harness files; it is an agent leaving its workbench in the deliverable.
That is a brief change (E11), not a `tree_diff` change: the recorder should not
be taught to hide files, because then it stops being evidence.

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

**Measured.** Run `36764071814` was the first on `2cb0dd1`, and its two
iterations disagree in a way that settles both open questions at once.

*Iteration 2 finished inside the 40-minute cap.* It took 3.9M tokens in
iteration 1 but completed here, and the 56 minutes of `sleep` that E8 measured
are gone. That confirms the diagnosis: the agent was not dawdling, it had never
been told how to run a batch (`MEASURE`), and importing the harness's own text
fixed it. **The sleeping was real and it is fixed.**

*Iteration 1 was killed by the 40-minute cap* (`stop=killed`, no edit, 0-byte
patch). So the remedy for cause 3 was wrong even though the diagnosis was right.
The cap was set from the arithmetic above — "near 30 min" per iteration — and
that arithmetic is dead: it came from removing the sleeps, and the run on which
it was based also happened to be a fast one. Against the eight historical
single-iteration runs (9, 42, 81, 87, 95, 96, 141, 153 min, median 91), a
40-minute agent ceiling truncates **more than half of all runs**, and the
truncation is silent: it produces a `NOT-A-WIN` for a tree the agent never got
to finish. A cap below the median is not a safety limit, it is a coin flip on
which runs produce evidence.

`AGENT_TIMEOUT_SECONDS` is now 150 minutes, which is not derived from anything
and is justified only by the job ceiling: at the 91-minute median, 2 × 150 +
scoring fits inside 360, and 3 × 150 does not.

**What this says about the brief generally.** The brief is the mutator's only
instruction channel, so a missing section is not a smaller prompt, it is a
wrong one. The three bugs that cost this loop the most — no `MEASURE`, and
earlier an empty first brief — were all omissions, not bad wording. When a
custom brief replaces a curated one, the first question is not "is mine
better?" but "what did theirs say that mine does not?"

**Not claimed.** 150 minutes is a guess that fits the ceiling, not a
measurement of what an iteration needs. If two iterations no longer fit in 360
minutes, the honest response is one iteration or checkpointing, not raising the
cap again — the first version of this cap was set from arithmetic that did not
survive contact with a run, and repeating that would be the same mistake twice.
The number of agent phases observed across successful runs is the thing to
derive the next cap from, and it has not been collected systematically.

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

**Cost.** Measured on the composed brief, both generated by the current
`brief.py` and differing only in `GAME_RULES.md`: **22285 → 26985 characters,
+4688 (+4.6 KB, +21.1%)**. The file itself went 8500 → 13200 bytes, and 52
creatures is more table than 14 death-derived rows. A fifth more prompt is paid
for the wider band, and it is not yet clear it is worth it; run `36764071814` is
the first to show whether the agent uses creatures outside the old death band.

## E10 — the artifact fallback was a promise, not a fact

**Change.** None to begin with. This is the finding, not a fix.

`36731664027` is the first run where publication failed, which is the only
condition under which the fallback matters. It was a lie.

`evolve.py` printed, on publication failure:

> results NOT published (…); **they are in the artifact**

The upload list at the time named `our-evolve.log`, `report.md`,
`preview-brief.md`, `runs/baseline.json`, `runs/history.json`, `runs/brief-*.md`
and `runs/transcript-*.log`. Nothing else. So on the one run that needed the
fallback, the artifact contained **no kept tree, no patches, no run record and
no results staging** — only the transcripts and `history.json`. The sentence was
written next to the code that writes the patches and did not describe the list
that uploads them. Two files, same repo, never compared.

The cost was not the log, which survived in `history.json`. It was
`runs/winner-2/` — iteration 2's kept tree, 0.0661, the best bot this project has
produced and the first kept tree it ever had. Gone, because the branch push
failed (E5) and the artifact was the other half of the promise. Also gone:
`runs/diff-001.patch`, `runs/diff-002.patch`, `runs/work-*/`, and the 22 KB
`log/wiz-hum-cha-mal-36731664027.json`.

**A second, independent loss, in the same run.** The run's own commit to `main`
was also rejected:

```
error: failed to push some refs to 'https://github.com/OlegPapulov/nethacker'
hint: ... have locally. This is usually caused by another repository pushing to
##[warning]push failed (concurrent run?)
```

That diagnosis was wrong. No concurrent run existed. `main` had moved because
*we* pushed `2cb0dd1` and `5849f59` about three hours into the run, after its
checkout. A four-hour loop on a moving `main` is routinely stale at the end;
the step assumed otherwise and swallowed the evidence under a warning that named
the wrong cause. `log/*.json` was committed locally and then lost with the
workspace.

**Fixes.** The artifact list now carries `log/*.json`, `runs/diff-*.patch`,
`runs/winner-*/` and `runs/work-*/`, so the fallback covers the things the
results branch would have carried. `Commit the verdict` fetches, rebases and
retries once instead of warning, and never forces. The `evolve.py` line now
names what the fallback actually is — "the kept tree and its patches are in the
30-day artifact" — because a fallback with an expiry is a weaker guarantee than
a ref, and saying so is the difference between a record and a rumour.

**What this says.** Both halves of "the results survive the job" were untested
against the one condition that matters: failure. E5's local test passed because
a laptop's credentials are global; E10's list was never read against the code it
was supposed to describe. Neither is a hard bug. Both are the same bug: a claim
about a fallback, written near the thing it depends on, verified by nothing.

## E11 — the agent ships its workbench inside the deliverable

**Change.** Proposed, not made. Needs a decision, so it is recorded here rather
than in a brief.

Iteration 2 of `36731664027` reported **61 changed files** to make a one-line
edit: `search_count ** 2 * 2` → `* 8`. Sixty were its own scratch —
`.tmpwork/agent.py.instrumented` (+1661), `.tmpwork/agent.py.orig` (+1560), 30
result JSONs, four diagnostic scripts. Iteration 1 left `direct_run.py` and
`local_eval.py` at the tree root. Both trees were kept or carried forward, so
this junk is now in the parent and will reach the hub.

This is not a `tree_diff` bug. The recorder is right: those files were added,
and a recorder that hid them would stop being evidence. It is also not really an
E7 bug — the stat *did* list the real file, fourth from last — though a 61-file
stat is close to as unreadable as no stat.

It is a brief problem: the agent was never told that `/workspace` is the
deliverable and not a workbench. The natural fix is one line in `HOWTO` — put
experiments in `/tmp`, and leave nothing in the tree that is not part of the
change. Cheap, and it improves the diff, the kept tree, and the hub submission
at once. Worth doing, but it is a brief change, so it should be dispatched and
measured like any other rather than landed on the strength of this paragraph.

## E12 — the loop could keep a tree that had lost 40% of its score

**Change.** Made. Three defects, one run, all in the judging path rather than the
brief, so nothing here is dispatched.

Run `36764071814` iteration 2 changed one file (`global_logic.py`, +23/-1) and
scored **0.0378 against a 0.0624 parent — a 39% regression.** It was kept. The
tree became the parent, and iteration 3 would have been measured against
0.0378, so the run would have drifted downward while every verdict said it was
holding the line. Nothing was published — `mean_gate` held — but the gate held
by accident, not by design, and the mechanism that let a 40% loss become the
parent was a documented policy in `paired_verdict`.

**1. Depth counted as progress.** `forward()` returned true if a seed's
`progress` rose *or* its `depth` rose *or* it survived longer at equal depth.
Iteration 2 reported **10 seeds "forward" and 10 "deeper"** — those 10 forwards
were depth, not score. `AGENTS.md` already records that depth is the wrong proxy
on this identity (`36615769123` climbed and lost 40%; `36637347806` found the
deciding family is XP on all 15 seeds), and `forward()` was still counting it.
`forward()` is now progress-only, and `deeper` is still counted and reported —
it is a fact about the run, just not a vote.

**2. `mean_gate` had one demotion, not two.** It demoted `WIN` → `KEEP` when
the mean did not improve, and that was the only branch that added "kept as the
parent". A tree that lost 39% therefore cleared the paired bar on fake forwards
and arrived at the keep branch. Reconstructed and verified against the run's own
seed rows: the shape now returns `NOT-A-WIN`, `fwd=0 back=14`.

**3. A capped turn was recorded as a failed hypothesis.** When
`AGENT_TIMEOUT_SECONDS` fired, `run_operator` caught the cancellation, logged
it, and returned the tree unchanged — which the loop then scored and filed as a
`NOT-A-WIN` it would "not repeat". Iteration 1 of that run is a run record
claiming the agent disproved something, when in fact the agent ran out of clock.
That is the wrong lesson in the one place the next iteration reads from. It is
now `TIMED-OUT`: not in `KEEPING_VERDICTS`, so the tree is reverted, with the
child's numbers and findings still recorded, because 16 episodes and 3.9M tokens
of observation are evidence even when the turn is truncated.

**The keep floor.** A material regression is now a **discard**, not a keep, with
`MEAN_KEEP_FLOOR = 0.9`. The threshold is taken from the noise, not from the one
bad run: one SE on this identity is 0.0109 against a mean of 0.0624, about 17% of
the mean, so a 10% dip is not resolvable at 15 seeds and `KEEP` is defensible,
while 39% is about 3.7 SE. Verified boundaries — 9 seeds forward with the mean
−7.5% returns `KEEP`; −11.3% and below returns `NOT-A-WIN`. The loop can still
hold a slightly-worse, more promising tree, which is the only reason `KEEP`
exists.

**A fifth thing, found by the tests.** The `KEEP` message blamed
`MIN_SEEDS_FORWARD` for splits that had cleared it: a 9-forward-6-back run is
`9 ≥ 5`, and it fails only the two-thirds shape, but the text said "short of the
5-seed bar". And `mean_gate` composed its verdict on top of a `why` that already
said "kept as the parent", so a discard read *"kept as the parent … so the tree
is reverted rather than carried forward as the parent"* — one sentence
asserting both dispositions. `paired_verdict` now reports only the paired facts
and `mean_gate` owns the disposition, so the two cannot contradict.

**Not claimed.** No timing is derived from this entry, and the floor has not been
tested against a real regression — it is calibrated against the noise band and
checked against the run's own seed rows, which is not the same as a run that
regresses on purpose. `MEAN_KEEP_FLOOR` is one constant if it proves wrong.

## Open

- E8 is now measured (see its entry): the sleeping is fixed by the `MEASURE`
  import, and the 40-minute cap that replaced it was truncating more than half
  of all runs. What is still missing is a systematic distribution of agent-phase
  durations, which is what the next cap should be derived from.
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
- E11 is a proposed brief change, unmeasured and not yet agreed.
- The loop has still never been kept over more than **one** iteration.
  `36731664027` kept its second tree, which is the first time the loop advanced
  its own parent, and then the job ended — so "can this compose improvements, or
  only accumulate findings" is still unanswered. It is now a cheaper question
  than it was, because E5 and E10 mean a kept tree survives the job.
