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
2. **Our experience entries for this identity** -- the observed failure modes,
   with the attempts already ruled out, so the model does not re-derive them.
3. **The previous attempts and what each scored** -- the stock
   `attempts.md` table, which the mutator already expects to exist.
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

REPO_ROOT = Path(__file__).resolve().parent.parent

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
"""


#: Sections about the HARNESS rather than the game are excluded from the brief.
#:
#: The first run sent 24,630 characters, of which 19,800 were our logs -- and
#: most of that was about the measurement apparatus: "per-turn tracing is
#: impossible inside the arena", "can the mutator see our notes?", "one job per
#: iteration". None of it tells the model anything about how the bot dies. It
#: is 80% of the reading spent on 0% of the decision, and it is a candidate
#: explanation for why one iteration cost 19.9 M tokens.
#:
#: A heading qualifies when it says the work was about how we measure, or about
#: the loop itself. Actual gameplay failures, measured baselines and hypotheses
#: about the bot are all kept.
_HARNESS_TOPICS = (
    "tracing", "trace", "infrastructure", "infra", "harness", "operator",
    "mutator", "concurrency", "provenance", "digest", "publish", "publishing",
    "artifact", "artifacts", "sign test", "power analysis", "classif",
    "our own loop", "determinism", "workflow", "runner", "x86", "arm64",
    "brief", "measurement", "cannot start", "loop",
)


def _is_harness_section(heading: str) -> bool:
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


def build(
    identity: str,
    diagnosis: dict | None,
    experience_text: str = "",
    experiments_text: str = "",
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
                "These are measurements from previous runs. Attempts listed as",
                "failed **have** been tried -- do not repeat them as if new.",
                "",
                *sections,
                "",
            ]

    if experiments_text:
        sections = _identity_sections(experiments_text, identity)
        if sections:
            parts += [
                "## Experiments already run on this identity",
                "",
                *sections,
                "",
            ]

    parts += [SCORING, HOWTO, CONTRACT]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("identity")
    parser.add_argument("--diagnosis")
    parser.add_argument("--experience")
    parser.add_argument("--experiments")
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
        read(args.experiments),
    )
    if args.out:
        Path(args.out).write_text(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
