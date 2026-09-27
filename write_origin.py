"""Write the provenance record for a `best/<identity>/` tree.

A bare `best/<identity>/` is unsafe. One was committed by a run that was then
cancelled, never replaced because nothing improved that cell, and later used as
a comparison baseline -- which made a stale tree look like a real 0.0126
measurement difference (N3b). Recording who wrote it, from what, and when turns
"stale leftover" into something a reader can check.

Kept as a file because a heredoc nested in a YAML `run: |` block has to be
indented to the block's own level, and a mistake there breaks the workflow file
outright rather than failing at runtime.
"""

from __future__ import annotations

import os
import pathlib
import sys


def main() -> None:
    identity = os.environ["IDENTITY"]
    destination = pathlib.Path("best") / identity
    destination.mkdir(parents=True, exist_ok=True)
    body = f"""identity:   {identity}
run:        {os.environ.get('RUN_ID', '?')}
iteration:  {os.environ.get('ITERATION', '?')}
parent:     {os.environ.get('PARENT', '?')}
seed_mode:  {os.environ.get('SEED_MODE', '?')}
written_by: evolve.yml, job "iter {os.environ.get('ITERATION', '?')}"

This is the tree `evolve` left in work/iter-0 for the iteration named above.
It is replaced on every successful iteration. Do NOT treat it as the current
best unless its `run:` matches the run you are comparing against -- a
cancelled or superseded run leaves its tree here, and a stale tree used as a
baseline is indistinguishable from a real measurement difference.
"""
    (destination / ".origin").write_text(body)
    print(f"wrote {destination / '.origin'}")


if __name__ == "__main__":
    sys.exit(main())
