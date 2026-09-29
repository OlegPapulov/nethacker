"""Compose the brief our operator receives, from OUR notes.

Why this file exists
--------------------
The stock brief (`nethackers.harness.brief.build_brief`) takes only
scores: identity, per-identity means, an overall, a target, the seeds, and an
optional wiki path. There is no free-text parameter, so nothing a human or a
sibling process has measured can reach the operator through it. The mutator
strips `AGENTS.md`, `CLAUDE.md`, `opencode.json` and friends from every tree it
hands to the agent, so notes cannot travel as files either.

That leaves exactly one sanctioned channel, and this file is it: **compose the
brief ourselves and hand the result to the operator.** `ContainerOperator.run`
takes `brief: str`, so the mutator does not care where the string came from.

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
5. **The contract**, verbatim from the project, so the model cannot break it.

Deliberately absent: any instruction about *what* to change. We know which
seeds die and how; we do not know the fix, and a hint that names a fix is a
hypothesis we have not tested. The brief supplies measurements and constraints,
and leaves the hypothesis to the operator -- which is the one job we want
delegated.

Usage: build_brief.py <identity> --diagnosis <diagnosis.json>
                       [--experience FILE] [--experiments FILE]
                       [--out FILE]
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

SCORING = """\
## How a change is judged

This is the part that is easy to get wrong, so read it carefully.

- `progress` is BALROG progression in [0, 1]: higher is better, and it rises as
  the bot survives, descends and advances.
- **The metric is coarse.** Across the 15 published seeds of a strong bot it
  takes only about **five distinct values**, because progression pins to
  milestone plateaus. Its standard error over 15 seeds is about **0.028**.
- Therefore a difference of means **cannot resolve a change of 0.01**, and any
  argument of the form "the average went up" is not evidence.
- A seed is a **complete, deterministic game**. So a change is judged **per
  seed**, candidate against parent, on the same seeds.
- **One seed can swing the score by 0.18.** So a change counts as an
  improvement only if **most seeds improve**, not if the average moved. In one
  real comparison a candidate gained +0.175 on one seed and lost -0.180 on
  another, and the mean of the two was +0.0013.
- Judge on **per-seed deltas and on the depth each seed reaches**, which is
   finer-grained than the progression value and is collected anyway.

### Depth is not progress

This is the mistake that has already been made here, and it is worth stating
plainly because the failure looks like a success.

Progression rises as the bot **survives and descends**. Those can move in
opposite directions: a change that reaches dlvl 4 in 4,000 turns instead of
dlvl 2 in 18,000 may be *worse* on the metric while looking obviously better on
any depth-ladder you reconstruct yourself. A real run did exactly this —
depth up, mean progression **down 40%** — and the change was reverted.

So when you reason about what a change will do, reason about **progression**,
which is what is scored, and treat depth as one input to it rather than as a
proxy for it. If your reasoning needs a value for progression that you cannot
observe, say that you are estimating rather than presenting the depth number
as if it were the objective.
"""

HOWTO = """\
## How to make your change

1. Make **one** focused change — a single idea, which may be a large diff.
2. Mark it with a `# hypothesis: ...` comment saying what you expect it to
   improve. The loop extracts that comment to attribute the change to you, and
   a change with no comment is recorded as unattributed.
3. Keep the contract working, and make sure the code imports cleanly.
4. **Do not tune to the seeds.** The seeds exist so changes are measured; a
   change that helps these 15 dungeons and nothing else will not transfer.
5. You have live Python and NLE. You may run a short foreground evaluation
   yourself to check the bot still works before you finish.

## Log what you found

Write your findings into **`/workspace/experience.md`**, appending one entry.
This is how the loop remembers: your worktree becomes the next iteration's
parent, so what you write here is what the next run will read before choosing
a change. An unlogged finding is a finding that will be re-derived from
scratch, or worse, re-attempted as if it were new.

Use this exact structure:

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

Tag the heading with **◆ gameplay** for what is about the game, or
**⛭ apparatus** for what is about the loop's own machinery. Untagged entries
are kept, so tagging is optional — but it is how a later run avoids spending
context on notes that do not describe how the bot dies.

**Write the entry before you finish, even if your change failed.** A failed
attempt with a measured result is worth more than a silent one: it is the only
thing that stops the next iteration from trying it again.
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


def _identity_sections(text: str, identity: str) -> list[str]:
    """Markdown sections about this identity, minus our own apparatus notes.

    Split on headings, keep any block naming the identity, and drop the ones
    whose heading is about how we measure rather than about the game. Crude on
    purpose: over-including real gameplay context is cheap, under-including it
    is not. Over-including *harness* context is not cheap, because it is the
    majority of the file.
    """
    out: list[str] = []
    for block in re.split(r"\n(?=#{1,3} )", text):
        block = block.strip()
        if not block or identity not in block:
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
