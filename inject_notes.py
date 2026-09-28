"""Inject our own experience and experiment log into the mutator's worktree.

Why
---
The mutator gives the operator a `/refs/` directory and a brief. The brief says
what to do; `/refs/` holds the parent bot, its per-seed eval, and the last few
attempts. **It contains none of our notes.** So an operator improving a bot has
no idea that ten seeds die on dlvl 1 to a goblin, that the champion for this
identity is at 0.1907, or that two previous mutations were already tried and
rejected. It re-derives what we already know, and spends 11 M tokens doing it.

Everything this project has learned sits in `experience.md` and
`experiments.md` in the repository, and none of it reaches the agent. This
script closes that gap.

What it does
------------
Copies a small, curated set of documents into the mutator's worktree, where the
operator will encounter them as files alongside the code it is editing:

* ``NOTES.md``  -- an index plus the entries relevant to this identity
* ``experience.md`` and ``experiments.md`` -- verbatim, if they exist

The notes are placed inside the worktree rather than passed on the command line
because the operator is a coding agent with a filesystem: a file is something it
reads, whereas a paragraph in a prompt is something it has to notice. It is
placed as a normal file in the tree, not hidden, so it is visible to any tooling
the agent runs.

Two honesty rules
-----------------
1. **The documents are written for humans and include known-wrong intermediate
   conclusions.** A file that says "the arena is deterministic" next to three
   experiments that said otherwise is actively misleading to a model. So the
   index states plainly that these are notes, that they contain superseded
   conclusions, and that the *per-experiment* Caveat fields carry the
   corrections.
2. **The tree must stay registerable.** ``nethackers.solution.json`` and
   ``bot.py`` are untouched, and the notes are added as new files. A solution
   carrying them is still a valid solution -- the arena loads ``bot.py`` at the
   tree root and ignores everything else -- but a run that produces a winner
   should have them stripped before it is published, because they are our
   bookkeeping, not part of the program. ``strip_notes`` does that.

Usage::

    inject_notes.py <worktree> <identity> [--repo-root DIR]
    strip_notes.py  <worktree>
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

#: Files we own and inject. The operator should read these before editing.
NOTE_FILES = ("NOTES.md", "experience.md", "experiments.md")

#: Where to find them: the repository this workflow checked out.
DEFAULT_REPO_ROOT = Path(".")

#: Files that must never be removed by strip_notes.
PROTECTED = ("bot.py", "nethackers.solution.json")


def _repo_root(argument: str | None) -> Path:
    return Path(argument) if argument else DEFAULT_REPO_ROOT


def _identity_entries(identity: str, text: str) -> list[str]:
    """The sections of a markdown file that mention this identity.

    Deliberately crude: split on headings, keep any block naming the identity.
    A heading may sit above its content, so a block is attributed to an identity
    if the block *or* the heading immediately before it names it. False
    positives are cheap here -- extra context does not mislead an agent the way
    missing context does.
    """
    blocks = re.split(r"\n(?=#{1,3} )", text)
    out: list[str] = []
    for block in blocks:
        if identity in block:
            out.append(block.strip())
    return out


def build_notes(identity: str, repo_root: Path) -> str:
    """Compose NOTES.md for one identity from whatever notes exist."""
    lines = [
        f"# Notes for improving `{identity}`",
        "",
        "These are working notes from the humans and agents iterating on this",
        "program. They are **notes, not instructions**, and they contain",
        "conclusions that later experiments overturned -- each experiment carries",
        "its own `Caveat` field recording the correction, so prefer the",
        "correction when the two disagree.",
        "",
        "Read these before editing. They exist so you do not re-derive what has",
        "already been measured, and do not re-try what has already failed.",
        "",
    ]

    experience = repo_root / "experience.md"
    experiments = repo_root / "experiments.md"

    if experience.is_file():
        text = experience.read_text(encoding="utf-8", errors="replace")
        blocks = _identity_entries(identity, text)
        lines += [
            "## Observed failures for this identity",
            "",
            *(blocks or ["_(no entry names this identity)_"]),
            "",
        ]
    else:
        lines += ["## Observed failures for this identity", "", "_(no experience.md found)_", ""]

    if experiments.is_file():
        text = experiments.read_text(encoding="utf-8", errors="replace")
        blocks = _identity_entries(identity, text)
        lines += [
            "## Experiments run against this identity",
            "",
            *(blocks or ["_(no experiment names this identity)_"]),
            "",
        ]
    else:
        lines += ["## Experiments run against this identity", "", "_(no experiments.md found)_", ""]

    lines += [
        "## How a change is judged",
        "",
        "- Scores are BALROG progression in [0, 1], higher is better, and it is",
        "  **coarse**: across the 15 published seeds it takes only ~5 distinct",
        "  values, so a difference of means cannot resolve a change of 0.01.",
        "- Your mutation is compared **per seed** against its parent, on the same",
        "  seeds. A seed is a complete, deterministic game.",
        "- A single seed can swing the score by 0.18, so a change is only a win if",
        "  most seeds improve, not if the average moved.",
        "- Propose **one** focused idea and mark it with a `# hypothesis:` comment",
        "  saying what you expect it to improve. That comment is how the change is",
        "  attributed to you rather than inherited from an ancestor.",
        "",
    ]
    return "\n".join(lines)


def inject(worktree: Path, identity: str, repo_root: Path) -> None:
    worktree.mkdir(parents=True, exist_ok=True)
    notes = worktree / "NOTES.md"
    notes.write_text(build_notes(identity, repo_root), encoding="utf-8")

    for name in ("experience.md", "experiments.md"):
        source = repo_root / name
        if source.is_file():
            shutil.copyfile(source, worktree / name)

    print(f"injected {', '.join(sorted(p.name for p in worktree.iterdir() if p.name in NOTE_FILES))}")


def strip(worktree: Path) -> None:
    """Remove the notes before a tree is published as a solution."""
    for name in NOTE_FILES:
        target = worktree / name
        if target.is_file():
            target.unlink()
    for protected in PROTECTED:
        if not (worktree / protected).is_file():
            raise SystemExit(f"refusing to strip: {protected} missing from {worktree}")
    print(f"stripped notes from {worktree}")


def main() -> int:
    if not sys.argv[1:]:
        print(__doc__)
        return 2
    command, target = sys.argv[1], Path(sys.argv[2])
    if command == "inject":
        identity = sys.argv[3]
        root = None
        if "--repo-root" in sys.argv:
            root = sys.argv[sys.argv.index("--repo-root") + 1]
        inject(target, identity, _repo_root(root))
        return 0
    if command == "strip":
        strip(target)
        return 0
    print(f"unknown command {command!r}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
