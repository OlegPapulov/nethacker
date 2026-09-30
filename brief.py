"""Compose the brief our operator receives, from OUR notes.

Why this file exists
--------------------
The stock brief (`nethackers.harness.brief.build_brief`) takes only
scores: identity, per-identity means, an overall, a target, the seeds, and an
optional wiki path. There is no free-text parameter, so nothing a human or a
sibling process has measured can reach the operator through it. The mutator
strips `AGENTS.md`, `CLAUDE.md`, `opencode.json` and friends from every tree it
hands to the agent, and runs the operator with memory disabled, so neither
files nor cross-run recall are channels.

That leaves exactly one sanctioned channel, and this file is it: **compose the
brief ourselves and hand the result to the operator.** `ContainerOperator.run`
takes `brief: str`, so the mutator does not care where the string came from.
`experience.md` and `GAME_RULES.md` do survive into the worktree and are worth
writing, but they are state rather than instruction -- the brief is the only
place an instruction can live.

What goes in, in order of usefulness to the model:

1. **The measured baseline for this identity** -- mean, per-seed rows, and the
   depth histogram, because "dies on dlvl 1 to a goblin" is a fact and "0.06" is
   not.
2. **The log the agent itself wrote** -- the `experience.md` entries from the
   parent tree, with the attempts already ruled out, so the model does not
   re-derive them. The brief also *tells* the model to write the next entry, so
   the log is a loop the agent closes itself rather than notes we maintain.
3. **The game facts** for this identity, from `GAME_RULES.md`, parsed from the
   NetHack 3.6.6 source the arena runs.
4. **The scoring rule that actually decides acceptance** -- the stock brief
   says "beat the average", which is wrong here: the metric takes ~5 distinct
   values across 15 seeds and one seed can swing 0.18, so the only usable
   statement is per-seed and a majority of seeds must improve.
5. **The loop itself** -- `HOWTO` states that the agent is one turn of an
   unsupervised loop, and that closing it (choose an experiment, try it, write
   the entry) is the job rather than a documentation step at the end.
6. **The contract**, verbatim from the project, so the model cannot break it.

Deliberately absent: any instruction about *what* to change. We know which
seeds die and how; we do not know the fix, and a hint that names a fix is a
hypothesis we have not tested. The brief supplies measurements and constraints,
and leaves the hypothesis to the operator -- which is the one job we want
delegated.

Usage: build_brief.py <identity> --diagnosis <diagnosis.json>
                       [--experience FILE] [--out FILE]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

def _find_repo_root(start: Path) -> Path:
    """The directory holding the loop sources and GAME_RULES.md.

    Searched upward, and the FIRST directory containing the script's own
    directory name wins over the filesystem root. This exists because the same
    module is run from two places -- the repository's ``loop/`` and a copy
    dropped at the repository root by CI -- and ``parent.parent`` is correct for
    the first and one level too high for the second. Searching upward alone is
    not enough either: from a copy at the repo root the only thing above it is
    ``/``, so the walk ran to ``/private`` and found nothing, and the brief
    silently lost every note in a run that otherwise reported success.
    """
    for candidate in [start, *start.parents]:
        if candidate.parent == candidate:  # reached the filesystem root
            break
        if (candidate / "loop" / "brief.py").is_file():
            return candidate
    # Fall back to the script's own directory's parent, which is the repo root
    # when the script lives in loop/.
    return start.parent


REPO_ROOT = _find_repo_root(Path(__file__).resolve().parent)

# The contract, as the project states it. Reproduced rather than imported so
# the brief stands alone if the package layout changes.
CONTRACT = """\
## The contract

- The bot lives at **`/workspace`**. Edit the strategy code in the
  `autoascend/` package, not the `arena_adapter.py` glue.
- `make_agent()` returns an object with `reset(observation)` and
  `act(observation) -> int`, where the int indexes `nle.nethack.ACTIONS`.
- Each episode is a fresh process, so all state lives on the instance.
- An exception, a bad action, or a timeout **zeroes that episode**, with no retry.
"""

GOAL = """\
## What you are working toward

**Ascend.** Win the game: descend the dungeon, take the Amulet of Yendor, and
escape through the five planes. No program on the leaderboard has done it yet,
so nothing here is a solved problem, and a score is a stand-in for progress
rather than the destination.

**The real objective is to get better at the game, and the score is only how
progress is counted.** Say so if a change makes the bot play better without
moving the number — that is worth more than it looks, and it is worth saying so
in your log, because a later turn cannot see it.

Two levels of objective, and it is worth being explicit about which you are
working on:

- **This turn: raise the score.** The loop measures progression and keeps what
  improves it. That is the thing you are judged on.
- **The project: ascend.** Every real win comes from a bot that understands the
  game better than the one before it — knowing what a monster is, what an item
  does, when a fight is winnable. A change that teaches the bot something true
  and general is worth more than one that squeezes a seed, even when only the
  second one moves the number this turn.

So aim at the mechanism, not the metric. "The bot now refuses to step on a
grid bug, because it is unkillable and deals ELEC" generalises; "the bot takes
the eastern corridor on seed 4" does not, and the leaderboard scores secret
dungeons rather than these fifteen.
"""

SCORING = """\
## How a change is judged

- `progress` is BALROG progression in [0, 1]: higher is better.
- A seed is a **complete, deterministic game**, so candidate and parent are
  compared per seed on the same seeds.
- **The metric is coarse.** It takes only about seven distinct values across
  15 seeds, because progression pins to milestone plateaus. One seed can swing
  the mean by 0.18. Judge on per-seed deltas, not on the average alone.
- **The loop keeps anything that improves the mean**, however small, and keeps
  it as the parent for the next iteration. A kept tree is not registered with
  the leaderboard, so there is nothing to lose by keeping a real but modest
  gain. Only a mean that went *down* discards the change.
- A `WIN` — the only thing that gets published to the leaderboard — additionally
  needs a clean per-seed majority, so that a result cannot be registered on a
  number that a single lucky seed carried.

### The ladder is XP, and depth is only one rung of it

This is the most important thing to know about the metric, and it is the
opposite of what the depth framing suggests.

Progression is `max(...)` over several milestone families — depth, **XP
level**, and others. On this identity's own 15 seeds, the family that decides
the score is **XP, on every single seed** — a seed that reached dlvl 8 still
scored its `Xp:11`, not its depth. A seed's depth and its score are therefore
not the same quantity, and optimising depth optimises a term that is often
*not* the maximum.

The consequence for your experiments: **the fastest route to score is XP
level**, and XP comes almost entirely from kills, not from items. The bot
currently spends its time avoiding fights, and the measured result is that the
monsters it coddles contribute only 1–8% of the XP while ordinary ones
(goblins, jackals, gnomes) contribute 73–97%. So "fight less" and "score more"
pull in opposite directions on this identity, and the resolve is not to stop
fighting — it is to fight things that are *winnable* and to survive the ones
that are not.

Which fights are winnable depends on the creature's `mov`, its movement points
per turn. Ordinary dungeon animals run 6 or 9; a wolf, jackal or grid bug is
12, a bat 22, a white unicorn 24. **Nothing on that list can be walked away
from** — a high value closes the gap you opened before your next turn. So
retreat is not a general answer here, and a strategy built on it is bounded by
how fast the killer is.

Two warnings, both learned the hard way here:

- **Depth is not progress.** A real run reached dlvl 3.80 instead of 2.27 and
  scored 0.0374 against a 0.0624 parent — a 40% regression while every depth
  number improved. Never present a depth number as if it were the objective.
- **The bot is gated.** Its descent rule requires `experience_level >= 8`
  before it will touch a staircase, so on dlvl 1 it must first grind kills up to
  that level. That gate is a deliberate design point to test, not a fact of the
  game — treat it as a hypothesis, and measure what changing it does to
  progression per seed rather than to depth.

If your reasoning needs a progression value you cannot observe, say you are
estimating. Do not present a depth number as the objective.
"""


HOWTO = """\
## You are one turn of a loop

You are not given a task and released. You are a single turn in a loop that
runs without supervision, and the loop closes through what **you** write down.

The cycle, which you should hold in mind while you work:

```
  experience.md  ->  an experiment  ->  a rewritten bot  ->  the loop plays it
   (what is known)   (one testable     (the change)        (15 seeds, measured)
                      claim)                                |
      ^                                                          |
      +------------------ you write this back ------------------+
```

Nothing else keeps that loop alive. There is no human reading your work and no
other process summarising it for you. If you do not write the entry, the next
turn of this loop starts blind: it will re-derive what you already derived,
and it may re-try what you already tried and measured as a failure.

So the work is not "edit the bot". It is: **decide what to try, try it, and
record what happened** — in that order, with the recording treated as part of
the job rather than as documentation you get to if there is time.

## 1. Read what is already known

`/workspace/experience.md` holds the log. Every entry there is a previous turn
of this loop that already thought about the bot on this identity. Read it
**before** choosing anything. An attempt listed as failed has been tried and
measured; repeating it wastes the iteration and produces a second data point
for a question that is already answered.

The file may be empty or absent on the first turn. That is the expected
starting state, not an error.

## 2. Choose ONE experiment

An experiment is a single falsifiable claim about why the bot scores what it
does, and a single change to test it. Not a list of improvements — one.

Good experiments are the ones that can come back **negative**. "Add a
danger-checking step before opening a door" is an experiment. "Improve
combat" is not, because nothing could show it failed.

Three things disqualify an experiment:

- **It cannot be measured.** If you cannot say what result would tell you it
  failed, it is not an experiment.
- **It is tuned to the seeds.** A change that helps these 15 dungeons and
  nothing else will not transfer to the secret dungeons the leaderboard
  actually scores you on. Prefer a change you believe would help *any* dungeon.
- **It chases depth.** See the ladder section: on this identity XP level
  decides the score and depth often does not. An experiment whose expected
  effect is "reaches dlvl N+1" is aimed at the wrong term.

Choose the experiment that attacks **the objective**, which is the score, via
**the mechanism**, which is something true about the game. If you find yourself
wanting a number to move rather than wanting the bot to understand something
better, that is the wrong experiment.

Say what you expect, before you look at the result, in the change itself:

```python
# hypothesis: <what you expect to improve, and why>
```

The loop extracts this comment to attribute the change to you. A change with
no comment is recorded as unattributed, which makes it impossible to learn
from later.

## 3. Rewrite the bot

Make the change in the `autoascend/` package — that is where the strategy
lives. `arena_adapter.py` is glue; changing it to compensate for a strategy
problem hides the problem.

Keep the contract working:

- `make_agent()` returns an object with `reset(observation)` and
  `act(observation) -> int`, where the int indexes `nle.nethack.ACTIONS`.
- Each episode is a fresh process, so all state lives on the instance.
- An exception, a bad action, or a timeout **zeroes that episode**, no retry.

You have live Python and NLE. Run a short foreground evaluation yourself to
check the bot still works before you finish. A change that crashes on load
scores zero and is indistinguishable from a bad idea.

## 4. Log what you found — this is not optional

**Append one entry to `/workspace/experience.md`.** Not a summary of the diff;
a record of the *reasoning*, because the diff is visible in the tree and the
reasoning is not.

The next turn of this loop reads this file before choosing anything. What you
write is the entire memory of this project.

```
## <YYYY-MM-DD> — <short title>

**Problem:**
<the situation that led to death or suboptimal progress>

**Hypotheses:**
- <possible cause #1>
- <possible cause #2>

**Attempts:**
- <what you tried first> → <result>

**What worked:**
<the change that helped, and the evidence — or "nothing yet">
```

**Put the identity in the heading, verbatim: `## <date> — <identity> — <title>`.**

This is not a style preference. The next turn's brief keeps only the entries
that name the identity it is playing, and drops the rest — the log is shared
across identities in the same tree, so an entry that does not say which one it
is about cannot be told apart from a note about a different character. A real
run wrote a complete, valuable entry and had it silently filtered out of the
following brief for exactly this reason.

Fill in **Attempts** even when you only got as far as one attempt, and fill in
**What worked** honestly. A failed attempt with a measured result is worth more
than a silent one: it is the only thing that stops the next turn from spending
its iteration on a question you already answered. "Nothing yet" is a valid and
useful answer. Leaving the section out is not.

Tag the heading with **◆ gameplay** for what is about the game, or
**⛭ apparatus** for what is about the loop's own machinery. Untagged entries
are kept, so tagging is optional — but it is how a later turn avoids spending
context on notes that do not describe how the bot dies.

### Do not revert your own change

**Leave your best measured change in the tree, even if you are unsure of it.**

Run `36637347806` made a real change and measured it at `0.0624 → 0.0671`, then
reverted it on the grounds that 3 seeds improved against 2 that got worse. The
loop never saw that measurement: by the time it scored the tree, the change was
gone, so the child was byte-identical to the parent and the iteration produced
`no seed moved on any signal` and nothing to learn from. A result you measured
and then deleted is indistinguishable from never having tried.

**This loop keeps any change that improves the mean**, even one seed's worth,
and even when the per-seed split is not a clean majority. A mean that went up is
a better place to search from, and a kept tree is not registered with the
leaderboard — so there is no board risk in keeping it. Only the flat mean and
the two-thirds split are reserved for a `WIN`.

So: measure it, and **keep the tree as it is**. If your own reading is that the
change is wrong, say so in *Attempts* and in *What worked* and let the harness
judge. Reverting is your decision only when the change is not runnable at all —
a crash on load, a broken contract, code that will not import. That is a
defect, not a judgement about the score.
"""


#: Sections about OUR APPARATUS rather than the game are dropped from the
#: brief. Measured: including them made the brief 80% harness notes -- "tracing
#: is impossible inside the arena", "two bugs that emptied the first brief" --
#: none of which tells the model how the bot dies.
#:
#: Keyword matching cannot separate them, because a harness entry quotes seed
#: numbers and so looks like a measurement. Tried: an E<digit>-is-harness rule
#: kept E2 and E6, both of which quote real scores while being entirely about
#: the apparatus. So the classification is EXPLICIT: an entry is marked
#: apparatus-only with a trailing "⛭ apparatus" on its heading, and marked
#: game-relevant with "◆ gameplay". Everything unmarked is kept, which is the
#: safe default -- a missing fact costs the model a hypothesis it might have
#: made anyway, while a present-but-irrelevant one costs tokens and dilutes the
#: facts that matter.
APPARATUS_MARK = "\u26ed apparatus"
GAMEPLAY_MARK = "\u25c6 gameplay"

_HARNESS_TOPICS = (
    "tracing", "infrastructure", "harness", "operator", "mutator",
    "concurrency", "provenance", "digest", "publish", "artifact", "sign test",
    "power analysis", "classif", "our own loop", "determinism", "workflow",
    "runner", "x86", "arm64", "brief", "measurement", "cannot start",
)


def _is_harness_section(heading: str) -> bool:
    if GAMEPLAY_MARK in heading:
        return False
    if APPARATUS_MARK in heading:
        return True
    low = heading.lower()
    return any(topic in low for topic in _HARNESS_TOPICS)


#: An identity as the project spells it: `role-race-align-gender`, four
#: hyphen-separated lowercase words, e.g. `wiz-hum-cha-mal`. Matched in log text
#: so a block naming a *different* identity can be told apart from one that
#: names none.
#:
#: Matched structurally rather than against a list of the 73 legal identities,
#: because a list goes stale the moment the project adds a role ("hea", "kni",
#: "mon" are not the ones a guess would produce) and a stale list fails open:
#: an unrecognised identity reads as "names no identity", so the block is
#: believed on its "this identity" wording alone. Four short words in a row is
#: not ambiguous with the surrounding prose.
_IDENTITY_RE = re.compile(r"\b[a-z]{3,4}-[a-z]{2,4}-[a-z]{2,3}-[a-z]{2,3}\b")

#: The unfilled form written into a fresh `experience.md`. It has to be
#: recognised from the angle brackets rather than from any one field, because an
#: agent that filled in the problem and the attempts but left the date or the
#: title blank still produced a block that is not a finding.
_PLACEHOLDER_RE = re.compile(
    r"<\.\.\.>|<YYYY-MM-DD>|<identity>|<short title>", re.IGNORECASE
)


def _identity_sections(text: str, identity: str) -> list[str]:
    """Markdown sections about this identity, minus our own apparatus notes.

    Split on headings, keep any block naming the identity, and drop the ones
    whose heading is about how we measure rather than about the game. Crude on
    purpose: over-including real gameplay context is cheap, under-including it
    is not. Over-including *harness* context is not cheap, because it is the
    majority of the file.

    The identity test is **exclusionary**: a block is dropped only if it names a
    *different* identity. Requiring it to name the right one was the original
    design, and it threw away good work twice over on run 36637347806 -- a 7 KB
    entry of real findings, carried forward correctly, dropped because it said
    "this identity" rather than "wiz-hum-cha-mal", and an entry naming no
    identity at all dropped for the same reason in the other direction. An entry
    that is thrown away silently looks identical to one that was never written,
    so the filter cannot depend on a model complying with a heading format.

    Inversion is safe because the log is read from the *parent tree*, which was
    seeded for this identity: a note in it is about this character by
    construction. A block naming another character is the genuine exception, and
    that is worth catching -- trees are shared and copied, so a note comparing
    against val-dwa-law-fem can end up in a wiz tree.

    The seeded placeholder written on the first turn is skipped, along with
    the file's own `#` title line. Both are the template rather than a finding,
    and a brief that repeats the form it is already showing spends the model's
    attention on it.
    """
    out: list[str] = []
    for block in re.split(r"\n(?=#{1,3} )", text):
        block = block.strip()
        if not block:
            continue
        if block.lstrip("# ").strip().lower().startswith("experience.md"):
            continue
        if _PLACEHOLDER_RE.search(block):
            continue
        named = set(_IDENTITY_RE.findall(block))
        if named and identity not in named:
            continue
        if _is_harness_section(block.splitlines()[0]):
            continue
        out.append(block)
    return out


def _depth_histogram(results: list[dict]) -> str:
    depths = [int(r.get("depth") or 0) for r in results]
    if not depths:
        return ""
    n = len(depths)
    on_first = sum(1 for d in depths if d <= 1)
    lines = [f"- **{on_first} of {n} seeds never leave dlvl 1.**"]
    for depth, count in sorted(Counter(depths).items())[:8]:
        lines.append(f"  - reached dlvl {depth}: {count} seed(s)")
    return "\n".join(lines)


def _death_table(results: list[dict]) -> str:
    rows = sorted(results, key=lambda r: int(r.get("turns") or 0))
    out = [
        "| seed | turns | deepest | progress | died of |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        out.append(
            f"| {r.get('seed')} | {r.get('turns')} | {r.get('depth')} | "
            f"{float(r.get('progress') or 0):.4f} | {r.get('death') or '-'} |"
        )
    return "\n".join(out)


# --- Game rules -----------------------------------------------------------
#
# E7: the brief carried measurements and constraints but no knowledge of the
# game, so the model could reason about the CODE and the DEATHS and still form a
# wrong hypothesis (E4: a correct-looking change that lost five seeds).
#
# GAME_RULES.md is generated from the NetHack 3.6.6 source, scoped to the
# identity being played and the creatures that actually killed a seed, so it
# answers "can a level-0 wizard win this fight" rather than "here is a manual".
# It is a FILE the model reads rather than prose in a prompt, which is the same
# reasoning that keeps the notes in the brief.
def game_rules_section(identity: str, repo_root: Path) -> str:
    path = repo_root / "GAME_RULES.md"
    if not path.is_file():
        return ""
    body = path.read_text(encoding="utf-8", errors="replace")
    return (
        "## The game itself\n\n"
        f"{body}\n\n"
        "These are the game's own numbers for the build you are playing, not "
        "approximations. Use them to decide whether a fight is winnable "
        "*before* you design the heuristic, rather than discovering afterwards "
        "that the fight was unwinnable."
    )



def build(
    identity: str,
    diagnosis: dict | None,
    experience_text: str = "",
) -> str:
    parts: list[str] = [
        f"# Improving the NetHack bot for `{identity}`",
        "",
        "You are improving a Python program that plays **NetHack** through the",
        "**NetHack Learning Environment**. Make **one** focused change that",
        "raises its score, and say why in a `# hypothesis:` comment.",
        "",
        GOAL,
        "",
    ]

    if diagnosis:
        results = diagnosis.get("results") or []
        mean = float(diagnosis.get("mean_progress") or 0.0)
        parts += [
            "## Where this bot stands",
            "",
            f"It scores **{mean:.4f}** mean progression over the "
            f"{len(results)} published seeds, and it never ascends.",
            "",
            _depth_histogram(results),
            "",
            "### Per-seed results",
            "",
            _death_table(results),
            "",
        ]

    if experience_text:
        sections = _identity_sections(experience_text, identity)
        if sections:
            parts += [
                "## What has already been observed about this identity",
                "",
                "These are entries previous runs of this loop wrote into",
                "`/workspace/experience.md`. Attempts listed as failed **have**",
                "been tried -- do not repeat them as if new. The file is in your",
                "workspace: read it before deciding anything.",
                "",
                *sections,
                "",
            ]

    rules = game_rules_section(identity, REPO_ROOT)
    if rules:
        # Before the scoring rule: what the game IS, then how you are judged.
        parts += [rules, SCORING, HOWTO, CONTRACT]
    else:
        parts += [SCORING, HOWTO, CONTRACT]

    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("identity")
    parser.add_argument("--diagnosis")
    parser.add_argument("--experience")
    parser.add_argument("--out")
    args = parser.parse_args()

    diagnosis = None
    if args.diagnosis and Path(args.diagnosis).is_file():
        diagnosis = json.loads(Path(args.diagnosis).read_text())

    def read(path: str | None) -> str:
        if not path:
            return ""
        candidate = Path(path)
        if not candidate.is_file():
            candidate = REPO_ROOT / path
        return candidate.read_text(encoding="utf-8", errors="replace") if candidate.is_file() else ""

    text = build(
        args.identity,
        diagnosis,
        read(args.experience),
    )
    if args.out:
        Path(args.out).write_text(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
