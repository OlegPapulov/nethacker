# Experiments on the brief

**Human-side log. Not the agent's.** The agent's memory is
`/workspace/experience.md` inside its own worktree; see `AGENTS.md`. This file
records one entry per *change to `loop/brief.py`*: what we predicted, why we
thought it, what the run did, and whether the prediction held.

**An experiment here must be able to fail.** A prediction that any outcome
would satisfy is not a prediction, and an entry whose outcome is "seemed fine"
has told us nothing. The cost is ~85 minutes of CI, which is the reason this
loop is manual: automation would generate changes nobody chose to make.

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

## E6 — does the experience log compose across five turns?

**Change.** None. This is a test of E1–E5 together, not a new brief.

**Prediction.** Over five iterations the log grows monotonically, later
hypotheses do not repeat earlier ones, and at least one iteration ends in a
`KEEP` — because the loop only learns from a kept tree, and three consecutive
`NOT-A-WIN`s with no keep would mean the loop is generating findings and no
progress.

**Result.** Run `36728246238` in flight. Settle it from
`python meta/summarize.py 36728246238`.

Note before reading it: that job has `timeout-minutes: 300` and five
iterations need about seven, so it will likely be cut off before
`publish_results` runs. If it is, the per-iteration history is still in the
artifact, and the honest verdict is **inconclusive on the `KEEP` prediction**
rather than "the loop cannot keep anything".
