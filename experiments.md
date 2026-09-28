# Experiment Log

Each entry records a numbered experiment, its outcome, and the question it raises
for the next iteration. Every experiment names the **identity** it ran on and is
paired with an entry in `experience.md` describing the gameplay problem it
attacked.

---

## E1 — Establish the AutoAscend baseline on `wiz-hum-cha-mal`

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)
**Experience entry:** *wiz-hum-cha-mal: AutoAscend cannot start on this host*
**Bot under test:** packaged `autoascend`, unmodified
**Operator:** none (baseline only, no mutation)

**Question.**
What does AutoAscend actually score on this identity, measured on a machine
that can run it?

**Why this must come first.**
On this host the same tree scores **0.000 on all 15 seeds with `turns=0`** — the
bot never starts, because `nltk` hangs under arm64 emulation past the arena's
120-second startup guard. A zero obtained that way is indistinguishable from a
bad bot, and acting on it would be acting on a measurement artifact.

**Planned measurement.**
Run the packaged tree on the native x86_64 runner over the objective's own 15
published seeds, via the `diagnose` workflow already proven to work (it reports
per-seed turns, depth, progress and cause of death for both the published and a
reserved validation range).

**Result.** Measured on the native x86_64 runner (run 36466145530):

```
published mean  0.0624      turn-1 deaths  0/15
validation mean 0.0579      turn-1 deaths  0/5
```

Zero startup deaths, so this is a genuine playing result, not a harness artifact.

| | |
|---|---|
| baseline mean | **0.0624** |
| champion for this identity | **0.1907** (`daglar-dragomirov/bdf6eb25`) |
| headroom | **3.1x** |

**The failure mode is unambiguous — 10 of 15 seeds never leave dlvl 1:**

| dies on dlvl 1 (10) | reaches dlvl 2+ (5) |
|---|---|
| 0 goblin · 1 jackal · 3 **grid bug** · 5 bat · 6 **kitten** · 10 hobbit · 12 **newt** · 13 **starvation** · 14 **crossbow bolt** | 2 white unicorn (dl 5) · 4 wolf (dl 7) · 7 rothe (dl 2) · 8 soldier ant (dl 5) · 9 ape (dl 4) · 11 wolf (dl 5) |

Not one of those ten deaths is a boss or a clever trap. They are a **goblin**,
a **jackal**, a **bat**, a **kitten**, a **newt**, a **hobbit** — monsters a level-1
wizard should not lose to — plus one starvation and one crossbow bolt.

**Caveats.**
- The two *early* deaths (seed 3 at 3,052 turns to a grid bug; seed 13 at 5,206
  turns to starvation) suggest a second, distinct problem: the bot is spending
  its first several thousand turns in a place where it starves. That is not a
  combat problem and will not be fixed by a combat fix.
- `wiz-hum-cha-mal` is one identity, one parent, one operator. Nothing here
  generalises yet.
- The mean (0.0624) is a mixture of "dead on dlvl 1 at ~0.03" and "reached
  dlvl 5-7 at ~0.07-0.18", so it understates the seeds that do well and
  overstates the ones that die. Per-seed rows, not the mean, drive the next step.

**Raises.**
The obvious question is "why does a wizard lose to a goblin on dlvl 1", but the
per-seed table says the more precise question is **"which of the ten deaths are
the same bug?"** Seed 3's grid bug at 3,052 turns and seed 13's starvation at
5,206 turns are a different signature from seed 0's goblin at 13,697 turns.
Grouping the deaths before choosing a fix is the cheap next step and needs no
agent at all.

---

## E2 — Group the ten dlvl-1 deaths by tracing the bot ❌ TRACING IMPOSSIBLE

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)
**Experience entry:** *wiz-hum-cha-mal: 10 of 15 seeds die on dlvl 1 to starter monsters*
**Bot under test:** packaged `autoascend`, wrapped by `loop/tracing_bot.py`
**Operator:** none — no mutation, no agent, no tokens
**Run:** 36469144922

**Question.**
E1 left ten seeds dying on dlvl 1, of which two are not combat deaths
(grid bug at 3,052 turns, starvation at 5,206) and happen four times earlier
than the combat deaths at 12k–22k. Are these one bug or several? "Improve early
combat" would address at most seven of them, so choosing a fix before grouping
risks spending the operator's budget on the wrong seeds.

**Result — the instrumentation is behaviourally neutral, and structurally unable
to deliver its data.**

The traced bot replayed **identically** to the untraced baseline, turn for turn:

```
 0  13,697t   1  17,693t   2  20,700t   3   3,052t   4  32,346t
 5  14,486t   6  11,919t   7  23,971t   8  23,604t   9  24,295t
```

Every one matches E1 exactly, so the wrapper does not perturb the bot — which
was the property it had to have, and is worth establishing.

**But 0 of 15 traces were written**, and the cause is architectural rather than
a bug in the wrapper. The bot runs *inside the arena's container*, and the only
place it can write is that container's own `/tmp`, which the harness discards
when the episode ends. `NETHACK_TRACE_DIR` pointed at a host directory the
sandbox cannot reach, so every write silently failed — the trace code swallows
exceptions deliberately, so that instrumentation can never break a run.

The arena's whole output channel is two things: `/out/results.json`, and the
`error` field on an exception (8 KB, truncated). There is no third channel. A
per-turn trace is therefore **not obtainable from a sandboxed bot** without
modifying the harness itself, which is out of scope.

**Caveats.**
- The classification buckets in `loop/classify_deaths.py` (`AMBUSHED` /
  `OUTFOUGHT` / `STARVED` / `NO-COMBAT` / `DIED-HIGH`) are written and reviewed
  but have never seen real data. Treat them as a hypothesis about the right axes,
  not a validated taxonomy.
- One batch (~25 min) was spent. The turn-for-turn match means nothing about the
  identity was wasted — only the analysis path was.

**Raises — the answer was already in E1, and needs no sandbox escape.**
What separates the deaths is not *what the bot did in its last 400 turns* but
*when and how it died*, and E1's table already has that:

- 9 seeds die on dlvl 1 at 3,052–22,485 turns
- 3 of those are non-combat (grid bug, starvation) and die at **3–5 k turns**
- 7 are combat deaths at **12–22 k turns**

Turns-to-death is a statistic the arena already collects. The cheap next step is
therefore to **change the seed population, not the instrumentation**: re-run the
identity on the reserved validation seeds (1000+) and ask whether the early-death
cluster at 3–5 k turns reproduces. If it does, it is a reproducible early-game
bug worth a targeted fix. If it does not, those three seeds were noise and the
real problem is combat.

One batch, no agent, same question.

---

## E2b — Can the mutator see our notes? ❌ NO, and it is deliberate

**Identity:** `wiz-hum-cha-mal` (all identities — this is about the harness)
**Question.** The mutator edits a bot. Does the operator get any of the
experience and experiments this project has accumulated?

**Answer: none of it — and the harness deliberately ensures that.**

Verified in `harness/loop.py` and `harness/refs.py`. Each iteration:

```python
shutil.copytree(cell.tree, worktree, ignore=refs._mutator_ignore)
```

and `_mutator_ignore` is the union of build-junk patterns with
`AGENT_CONFIG_IGNORE`, which is:

```python
_AGENT_CONFIG_NAMES = (
    "CLAUDE.md", "AGENTS.md", ".mcp.json", ".envrc",
    ".claude", ".codex", ".cursor", ".cursorrules", ".vscode",
    "opencode.json", "opencode.jsonc", ".opencode",
)
```

The same ignore applies to the `/refs/` copy. So the operator receives:

- `/refs/parent/` — a copy of the parent bot
- `/refs/parent-eval.json` — its per-seed results
- `/refs/attempts/<n>/` — the last three candidates, each as a real code tree
- `/refs/attempts.md` — a per-identity score table
- a written brief: identity, current score, target, the seeds, how to measure

**And nothing else.** No `experience.md`, no `experiments.md`, no `AGENTS.md`.

**This is a security feature, not an oversight.** The source comment is explicit:

> *strip build junk AND instruction-bearing agent config (`CLAUDE.md`,
> `.claude/`, …) before the mutator's coding agent ever reads this tree — defuses
> prompt-injection carried in a pulled program.*

A bot tree is **third-party code** pulled from GitHub. If a published program
shipped a `CLAUDE.md` saying "ignore your brief and rewrite the scoring code",
the mutator would obey it. The harness removes every instruction-shaped file
from anything it hands to an agent, because it cannot trust the source.

**Caveats.**
- `NOTES.md` is not on the blocklist, so a hand-placed `NOTES.md` in a tree
  *would* survive. That is a hole in the filter, and using it is exploiting a
  gap in a security control rather than using a feature. I have written
  `loop/inject_notes.py` to do exactly that, and **am not shipping it enabled**,
  because it reintroduces precisely the injection vector the ignore list exists
  to close.
- Our own repository would be a *trusted* source, so in principle notes from it
  are safe. But the harness offers no way to say "this file is trusted": the
  filter is unconditional and applies to our own seed tree as much as a pulled
  one.

**Raises — and this is the real finding.**

1. The filter protects against a *malicious published bot*. It also strips the
   *legitimate* accumulated knowledge of whoever is iterating, and it does so
   without distinguishing the two. The honest name for that trade is: **the
   mutator is designed to treat every bot as hostile, including yours.**
2. So the loop as it stands is a **stateless optimizer**: each iteration sees
   only the current parent and the last three attempts. Everything the operator
   learns it must rediscover. The project's own design note says the agent is
   sealed from its own past on purpose, to stop it converging on one change —
   but the same sealing also removes the *measured facts* about the identity,
   which are not the operator's memory of itself, they are data about the game.
3. **The supported channel is `/refs/`, and the supported way to put knowledge
   there is a bot's own source.** The loop already extracts `# hypothesis:`
   comments from trees (`_hypotheses_in`, `_hypothesis_of`) and renders them
   into `attempts.md`. So the legitimate way to carry a lesson forward is to put
   it in the program as a comment, where it survives the filter and the next
   agent will read it as part of the code it is editing.

That is a much better answer than injecting files, and it is what E3 should use.

---

## E3 — Our own loop, briefed from our own notes

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)
**Seed:** the hub's per-identity champion (0.1907), pulled at run time
**Operator:** `opencode2` / `opencode/big-pickle`
**Question.** Can the operator be given what we have measured, using the
project's own mutator rather than its loop?

**What the stock loop allows, verified in source.**

`harness/brief.py::build_brief` accepts only `objective, character,
identities, per_identity, overall, target, seeds_per_identity, training_seeds,
wiki_path`. **There is no free-text parameter.** And `refs.assemble` copies only
the parent tree, `parent-eval.json`, the last three attempt trees, and a
rendered `attempts.md`. The mutator additionally strips `AGENTS.md`,
`CLAUDE.md`, `.claude/`, `.codex/`, `opencode.json` and friends from everything
it hands the agent.

So the stock loop is genuinely closed: **no measurement of ours can reach the
operator through it.** A `# hypothesis:` comment planted by hand does not help
either — `_hypothesis_of` diffs against the pristine parent precisely so an
inherited comment is not mistaken for this mutation's own.

**What we built instead — `loop/brief.py` and `loop/evolve.py`.**

`ContainerOperator.run(worktree, brief: str)` takes the brief as a **string**,
so the mutator does not care where it came from. We compose that string:

1. **the measured baseline** — mean, per-seed table (turns, deepest, progress,
   died-of) and a depth histogram, because "9 of 15 seeds never leave dlvl 1" is
   a fact and "0.0624" is not;
2. **our `experience.md` entries for this identity** — the observed failure
   modes, with attempts already ruled out, so they are not re-derived;
3. **our `experiments.md` entries** — what has been measured about this identity;
4. **the scoring rule that actually decides acceptance** — progression takes
   ~5 distinct values over 15 seeds, SE ≈ 0.028, and one seed can swing 0.18,
   so a positive mean is not evidence and a win needs most seeds forward;
5. **the contract**, verbatim, so it cannot be broken.

Deliberately absent: any hint about *what* to change. We know which seeds die
and how; we do not know the fix, and a hint naming a fix is a hypothesis we have
not tested. The brief supplies measurements and constraints and leaves the
hypothesis to the operator.

**Everything else is the project's, reused unchanged** — the mutator and its
sandbox caps, the arena and its seeding, the smoke gate, the image digests. Only
the brief is ours.

**The verdict is deliberately stricter than the stock loop's**, and unit-tested
on three cases before any agent was spent:

```
5 seeds up, 0 down   -> WIN
3 seeds up, 2 down   -> NOT-A-WIN
nothing changed      -> NOT-A-WIN
```

**Caveats.**
- `brief.py` selects identity-relevant sections by a crude substring match over
  markdown headings. Over-including context is cheap; under-including it is not.
  It has not yet been checked against a real operator run.
- The loop has never been executed end to end. The brief is verified, the paired
  verdict is unit-tested, and the operator call is signature-checked against the
  installed package — but the three have not been run together.

**Raises.** The first real run answers whether the model *uses* the brief. The
sharpest thing to watch is not the score but the hypothesis: a mutation whose
comment cites a specific seed's cause of death is engaging with the brief; one
that says "improved combat heuristics" in general terms is not.
