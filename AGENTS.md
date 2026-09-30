# The mutator loop — how this repository works

This is the harness for an agent that improves a NetHack bot without human
supervision. It is not documentation of a finished design; it is the design,
written down so the next person changing it knows what they are changing.

## What this project is

[NetHackers](https://nethackers.dunnolab.ai) is an open effort to build the
first program that reliably **wins NetHack 3.6.6** — ascends, not merely
survives. That is the objective; everything else here is machinery pointed at
it.

Two things about the arena are easy to get wrong, because they invert what a
normal optimization loop assumes:

- **The score is a stand-in, not the goal.** Programs are ranked by BALROG
  *progression* on [0, 1], and no program on the board has ascended. A rising
  number is evidence of progress toward a win; it is not a win. A change that
  teaches the bot something true and general is worth more than one that
  squeezes a seed, even when only the second moves the number.
- **The seeds you tune against are not the seeds you are scored on.** The 15
  published seeds are self-reported; the leaderboard re-runs submitted programs
  on secret dungeons. So a change that only moves the fifteen is not a change,
  it is an overfit, and the harness can only partly tell the difference. This is
  the single biggest reason to keep the loop honest about mechanisms.

Scores are also coarse and noisy in a specific way: 15 seeds, one of which can
swing the mean by 0.18, and a measured standard error around 0.011 on this
identity. See "What the metric will not tell you" below.

## The cycle

One iteration, from `loop/evolve.py`:

1. **Fetch a seed.** The bot to improve, from the hub, a pinned ref, or the
   packaged AutoAscend root.
2. **Score the parent** on the 15 published seeds. This is the baseline every
   later number is compared against.
3. **Compose a brief** (`loop/brief.py`) from the baseline, the identity's
   `experience.md` entries, and `GAME_RULES.md`.
4. **Hand the brief to the mutator agent** in a container, with the tree
   bind-mounted at `/workspace`. The agent edits the bot and leaves a
   `# hypothesis:` comment saying what it expects to improve.
5. **Smoke test**, then **score the child** on the same 15 seeds.
6. **Judge** — `paired_verdict`, then `mean_gate`.
7. **Keep or discard.** A kept tree becomes the next parent, so the run carries
   its own progress forward. A discarded tree is binned — but its `experience.md`
   is harvested into the surviving parent, so a failed experiment still stops
   the next iteration from repeating it. Either way the edit itself is
   recorded as a patch (`diffs/<n>.patch`), which for a *discarded* mutant is
   the only surviving copy of the code it wrote.
8. **Publish a win.** A `WIN` is pushed to its own branch and registered with
   the leaderboard. **Only a `WIN` is registered.** A `KEEP` is a better place
   to search from, not a better bot, and registering a 0.06 beside real entries
   would misrepresent the work.
9. **Publish the run's results.** Whatever the verdicts, the run pushes the
   surviving parent's `experience.md`, its `history.json`, every kept winner
   tree, and `diffs/*.patch` to a per-run
   `evolve-result/<identity>-<run_id>` branch. This is a record, not a
   submission, and the next run does not read it — runs stay independent by
   design.

Then it repeats, or the run ends. One iteration is not a fixed cost — eight
single-iteration runs took 9 to 153 minutes, median 91 — and most of that is
the agent, not the scoring. See "Running it" before choosing a count.

## The two rules that make it work

**A result is only a result if the mean moved.** `paired_verdict` asks whether
most seeds moved forward; `mean_gate` asks whether the batch average improved.
Both must hold for a `WIN`. This is not belt-and-braces — it is the case the
apparatus exists to catch. Run `36615769123` produced 10 seeds forward, cleared
two-thirds *exactly* (`3×10 = 30 ≥ 2×15 = 30`), and scored 0.0374 against a
0.0624 parent. Depth went up; progress went down 40%. The old rule published it.

**Depth is not progress, and the reason is sharper than "it also rewards
survival."** `progress` is BALROG progression in [0, 1], scored as a `max(...)`
over milestone families — depth, XP level, and others. The mutator cannot see
the scorer, so it reconstructs a proxy and optimizes that. In `36615769123` it
chose depth, and depth was a *plausible* proxy: the run did climb, and scored
0.0374 against 0.0624. Run `36637347806` then read the scoring code and found
the family that actually decides the number on this identity is **XP, on every
one of the 15 seeds** — a seed that reached dlvl 8 still scored on its XP.
Both facts matter: depth is not the metric, and *neither is surviving*. Chasing
turns is as wrong as chasing depth.

## The files

| file | role |
|---|---|
| `loop/evolve.py` | the loop: seed → brief → agent → score → judge → keep; also `harvest_log` and `tree_diff` |
| `loop/brief.py` | composes the operator's brief; the only channel to the agent |
| `loop/register_evidence.py` | builds the evidence payload `nethackers register` requires |
| `loop/register_winner.py` | pushes a `WIN` and registers it; also pushes per-run results branches; never raises |
| `loop/build_game_rules.py` | generates `GAME_RULES.md` from the NetHack 3.6.6 source |
| `log_verdict.py` | writes `log/<identity>-<runid>.json` — the committed record of a run |
| `experience.md` | **written by the agent**, inside the worktree, per iteration |
| `GAME_RULES.md` | game facts parsed from source, scoped to the identity |
| `.github/workflows/our-evolve.yml` | runs the loop in CI, with the auth gate |
| `meta/experience.md` | **written by us**: what steering the mutator has taught us |
| `meta/experiments.md` | **written by us**: one entry per brief change, with its outcome |
| `meta/summarize.py` | read-only; prints the run table from `log/*.json` |

`meta/` is the *human* half of the loop and is deliberately not a
`experience.md`. The agent's log lives in the tree, because the tree is what
carries it. Ours records a different subject — what we have learned about
steering the mutator, by changing the brief and watching what happened — and it
is **never** spliced into a brief or read by the agent. `1056dd4` removed the
repo-root `experience.md` and `experiments.md` precisely because a log the
harness maintains and the agent merely reads is the wrong division of labour;
reusing those two names at the root would invite putting them back into the
brief.


Root copies of the `loop/` modules exist and are byte-identical. The workflow
copies them beside `evolve.py` because the agent's imports resolve from there.
**If you edit one, copy it to the other** — a stale root copy imports last
iteration's code and silently does the old thing.

## Why `AGENTS.md` cannot instruct the mutator

`AGENTS.md` looks like the obvious way to instruct the mutator agent, and it is
not — even though this file exists and is read by every person and agent
working *on* the loop. The mutator **strips it**: `harness/refs.py` lists
`CLAUDE.md`, `AGENTS.md`, `.mcp.json`, `opencode.json` and friends in
`_AGENT_CONFIG_NAMES` and passes them to `shutil.ignore_patterns`, so they are
removed from the copy of the tree the agent receives — not hidden, deleted.

The reason is prompt-injection defense. A bot tree is fetched from the
leaderboard, and if any published tree could carry its own `AGENTS.md`, a
malicious submission could hand the mutator instructions and hijack the loop.
The list is applied to every copy that feeds the agent, worktree and `/refs/`
alike, so there is no supported way around it.

**The brief is the channel.** `ContainerOperator.run(brief=...)` takes a string
and the mutator does not care where it came from, so `loop/brief.py` composes it
and everything the agent must know travels in that one string. `CONTRACT`,
`GOAL`, `SCORING` and `HOWTO` in `brief.py` are the agent's standing
instructions, and they are maintained there rather than in a file the agent
would ignore. The baseline numbers and `GAME_RULES.md` are appended by `build`.

`GAME_RULES.md` and `experience.md` *do* survive into the worktree, and the
agent can read them. Verified against `_mutator_ignore` — they pass, while
`AGENTS.md` and `opencode.json` do not.

## `experience.md` is the memory, and the tree is what carries it

The agent writes its own entries, following the template in the brief, into
`/workspace/experience.md` during the iteration. Because the parent is
`shutil.copytree`'d into the next worktree, and a kept winner becomes the next
parent, **the log travels with the bot automatically**. A `KEEP` carries its
written experience forward; a `NOT-A-WIN` tree does not — it is binned — so
`harvest_log` copies that mutant's *new* entries into the surviving parent
instead. It matches on entry headings and takes only blocks the parent has not
seen, because the mutant was seeded from that parent and its log necessarily
begins with all of it.

This is why the log lives in the worktree and not in the repository root: the
repository holds the harness, the worktree holds the state. Keeping the log in
the repo would require a separate mechanism to decide which iteration's log
belongs to which parent, and the copytree already answers that.

Two boundaries are worth stating because they are easy to assume otherwise.
`harvest_log` covers iteration to iteration, and `publish_results` covers the
end of the *run* — without the second, run `36710578461` lost 4186 characters
of findings (two real defects in the bot's corpse handling) to a workspace that
died with the job. Neither makes runs depend on each other: each run seeds
fresh from the hub and re-derives what it needs.

## `tree_diff` records the edit, because the report is not the edit

The agent's log records what it *says* it changed. Run `36637347806` said it
fixed starvation; `36710578461` said the same about corpses, with file and line
numbers. Neither claim was checkable afterwards, because the mutant's tree is
binned on `NOT-A-WIN` and only the kept tree survives. What was left was a
paragraph of the mutator's own prose describing code that no longer existed
anywhere — the weakest possible record of a failed experiment, because it is
unfalsifiable and its author has an interest in it reading as thorough. It is
also how the loop ended up repeating "9 of 13 killers have mmove 12 (max
speed)" in the brief: a number from a discarded tree, repeated because it was
in writing and nobody could check it against the source.

So each iteration diffs the worktree against the parent it was seeded from
(`tree_diff`), prints a per-file stat, and writes `diff-<n>.patch`. The trees
are plain directories — no `.git` — so it is a `difflib` walk, not `git diff`.
Three details matter:

- **The stat is never truncated; the patch may be.** `changed` decides what to
  look at, so it has to be complete. The patch is a record, not a copy, so it is
  capped at `DIFF_CHARS` and flagged when it is.
- **Harness files are excluded.** `experience.md`, `brief-*.md`,
  `transcript-*`, `history.json` and `__pycache__` are not the mutator's edit.
  The agent rewrites its log every turn, so including them would bury the one
  change worth reading — a diff full of prose is a diff nobody reads.
- **Binary files are skipped, not mangled.** A file with NUL bytes or over 2 MB
  is reported as unchanged rather than diffed as text.

Both artifacts reach the results branch, so a run's record contains the code, not
just the claim about it. This does not make the mutator trustworthy — an agent
can still describe an edit it did not make, and the patch only bounds how long
that gap survives.

## Updating the brief

`loop/brief.py` is the only channel to the mutator, so it is also the only
place a standing instruction can live. Two rules follow, and the second is the
one that is easy to get wrong.

**1. When a brief change reflects a design decision, record the decision here
as well as in `meta/experiments.md`.** This file is the drift guard: it is
written for the next person, and a brief edit with no recorded reason is a
brief edit nobody can evaluate later. The loop is
experience → experiment → rewrite, and the rewrite is to `brief.py`; what the
rewrite *taught* is what belongs in `meta/experience.md`.

**2. The brief must never point the agent at `AGENTS.md`, at `meta/`, or at
any other file here.** All of them are absent from the tree the mutator
receives — `AGENTS.md` and the agent-config files by `_AGENT_CONFIG_NAMES`, and
`meta/` because it is simply not in the tree. An instruction to "see
`AGENTS.md`" is an instruction to a file that does not exist, and the agent
will either ignore it or invent its contents. The brief is self-contained by
construction; keep it that way.

Statistics quoted in the brief and here are measured, and they go stale. Both
"about five distinct values across 15 seeds" and the SE figure were wrong at
the time of writing. Re-derive them from `log/*.json` with `meta/summarize.py`
rather than copying a number forward.

## Running it

```bash
gh workflow run our-evolve.yml -f identity=wiz-hum-cha-mal -f iterations=2
```

**Ask for 2 or 3. Do not ask for more, and know why.** One iteration is not a
fixed cost: eight successful single-iteration runs took 9, 42, 81, 87, 95, 96,
141 and 153 minutes — median 91, with a tail past 2.5 hours. The job's
`timeout-minutes` is 360, which is not a tuning choice: it is the hard ceiling
for a GitHub-hosted job, and Support cannot raise it. Three iterations fit at the
median, two fit with real headroom, and four do not fit even at the best time
observed. An earlier version of this file claimed ~30–45 minutes per iteration,
which is what made a five-iteration request look reasonable; it was wrong by
about 2×, and the cost of believing it was a run that produced nothing.

That matters because **a job killed by the timeout produces nothing at all.**
`Upload everything` and `Commit the verdict` are steps *after* `Run our loop`,
so they never execute. No artifact, no results branch, no committed record —
the iteration in flight is the unit of loss, and the run is not checkpointed
anywhere. `runs/history.json` in the artifact is worth reading *when there is
an artifact*, which a timeout denies you.

Registration is opt-in by credential. Add two repository secrets:

- `NETHACKERS_TOKEN` — a **classic** PAT, scope `public_repo`, no expiry
- `NETHACKERS_LOGIN` — the login it belongs to

`nethackers whoami` gates it before an iteration is spent, so a bad token
degrades to "keeps trees, publishes nothing" instead of silently discarding
every candidate. Do **not** paste the `access_token` from `nethackers login`:
it expires in about eight hours, and `write_credentials.py` records no expiry,
so the CLI would treat a dead token as permanent and never refresh it.

## What the metric will not tell you

Fifteen seeds is a noise floor, not a sample. On `wiz-hum-cha-mal`'s baseline
the measured SE is **0.0109** (`sd 0.0420 / √15`), progression takes **7**
distinct values across the 15 seeds, and one seed can swing the mean by 0.18.
A change of 0.01 is not resolvable at this batch size, which is why a `WIN`
needs the per-seed shape *and* a moved mean *and* is easy to lose by a mechanism
that is real but small. The mutator agent's own response to this — measuring on
held-out seeds it did not tune against — is the right instinct, and the harness
does not yet do it automatically.
