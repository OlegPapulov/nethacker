"""Publish the evaluated tree to `best/<identity>/`, keyed by its digest.

Why this exists
---------------
`best/<identity>/` is the tree the next iteration inherits and the tree a
confirm run scores. Three separate ways it could be the wrong artifact, all of
which happened:

1. **Never invalidated.** A tree committed by a run that was then *cancelled*
   stayed there forever, because nothing had ever improved that cell. It was
   later used as a comparison baseline and read as a 0.0126 measurement
   difference (N3b).
2. **Not the tree that was evaluated.** The loop's own `child_digest` is the
   digest of the candidate it *scored*. The tree that lands in `work/iter-0` is
   a working copy and is not always byte-identical to it -- in N4 the loop
   reported `c29ab883` while the committed tree hashed to `aa9cce20`. So
   `best/` was holding something the loop had never measured, and everything
   downstream confirmed the wrong bytes.
3. **No record of provenance.** Nothing said which run wrote it, so a leftover
   was indistinguishable from a current best.

The fix is to key the directory by the digest the loop reported, and refuse to
publish a tree whose digest does not match. If they disagree, say so loudly and
write nothing -- a `best/` that is known-stale is better than one that is
confidently wrong.

Run with the digest from the loop's metrics as argv[2]; empty to skip the check.
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import sys


def solution_digest(tree: pathlib.Path) -> str:
    """The digest `nethackers.eval.runner._solution_digest` computes."""
    from nethackers.eval.runner import _solution_digest

    return _solution_digest(tree)


def loop_child_digest(latest_runs: pathlib.Path) -> str | None:
    """The `child_digest` the loop recorded for this iteration, if any."""
    metrics = latest_runs / "metrics.jsonl"
    if not metrics.is_file():
        return None
    for line in metrics.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if row.get("child_digest"):
            return str(row["child_digest"])
    return None


def main() -> int:
    # `--print-digest` lets the workflow read the loop's own child_digest
    # without embedding a python heredoc in a YAML `run: |` block, which has
    # broken the workflow file outright twice in this project.
    if sys.argv[1:2] == ["--print-digest"]:
        print(loop_child_digest(pathlib.Path("runs/runs/latest")) or "")
        return 0

    source = pathlib.Path(sys.argv[1])
    identity = sys.argv[2]
    expected = (sys.argv[3] if len(sys.argv) > 3 else "").strip()

    if not (source / "bot.py").is_file():
        print(f"::warning::no bot.py under {source}; not publishing a best tree")
        return 0

    if expected:
        try:
            actual = solution_digest(source)
        except Exception as exc:  # noqa: BLE001 - report, never crash the step
            print(f"::warning::could not digest {source}: {exc}")
            return 0
        if actual != expected:
            print(
                f"::warning::NOT publishing best/{identity}: the tree in work/ hashes "
                f"to {actual} but the loop scored {expected}."
            )
            print("::warning::Publishing it would make every later confirm score a "
                  "tree the loop never evaluated.")
            return 0
        print(f"digest matches the loop's child_digest: {actual}")
    else:
        print("::warning::no child_digest recorded; publishing without a digest check")

    destination = pathlib.Path("best") / identity
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    shutil.copytree(source, destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    (destination / ".origin").write_text(
        f"""identity:   {identity}
run:        {os.environ.get('RUN_ID', '?')}
iteration:  {os.environ.get('ITERATION', '?')}
parent:     {os.environ.get('PARENT', '?')}
seed_mode:  {os.environ.get('SEED_MODE', '?')}
digest:     {expected or '(unchecked)'}
written_by: evolve.yml, job "iter {os.environ.get('ITERATION', '?')}"

This is the tree the loop scored, verified by digest. It is replaced on every
successful iteration. Do NOT treat it as the current best unless its `run:`
matches the run you are comparing against.
"""
    )
    print(f"published best/{identity} ({len(list(destination.rglob('*.py')))} python files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
