"""Write a run's verdict to `log/<identity>-<runid>.json`, and nothing else.

Why this file exists
--------------------
`runs/` and `our-evolve/` used to be committed. They held 417,829 of the
repository's 417,978 tracked files: a private copy of autoascend under
`work-*/` per iteration, the 1.6 MB transcript, the winner trees. One cancelled
run put 13.6 M lines of that back on `main` on its way out, and a full clone
reached 6 GB. A repository that costs 6 GB to check out is a repository people
stop cloning, and the 149 files that are actually the loop get lost in it.

So the trees and the transcripts are gone from git. What stays is the part worth
keeping per run, and it is small: the verdict the loop reached, the baseline it
measured against, and whether a transcript was captured at all. A few hundred
bytes. The full transcript and the mutated tree stay in the workflow's own
artifacts for 30 days, which is where you go when a run needs explaining.

What must never happen again
----------------------------
A run that spends 17.7 M tokens and returns the tree unchanged is the case this
record exists to make legible. E8 spent 10.0 M and left nothing; the two runs
after it spent 17.7 M each and were only readable by digging the transcript out
of the artifact by hand. `transcript` below is the flag that says whether that
dig is worth doing.

Written as a file rather than a heredoc inside the workflow's ``run: |`` block,
for the same reason `write_credentials.py` is a file: a heredoc nested there has
to be indented to the block's level, and a mistake only surfaces as a mid-job
runtime failure.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys

#: Enough to tell a null result from a crash, not enough to fill a repository.
REPORT_CHARS = 4000


def read_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def verdict(work: pathlib.Path) -> dict:
    out: dict = {
        "run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "identity": os.environ.get("IDENTITY", ""),
        "operator": os.environ.get("OPERATOR", ""),
        "model": os.environ.get("MODEL", ""),
        "conclusion": os.environ.get("CONCLUSION", ""),
        "transcript": any(work.glob("transcript-*.log")),
    }
    history = read_json(work / "history.json")
    if history is not None:
        out["history"] = history
    baseline = read_json(work / "baseline.json")
    if baseline is not None:
        out["baseline"] = baseline
    return out


def trim(entries) -> None:
    """Keep the operator's own words, but not all 4000 characters of them."""
    if not isinstance(entries, list):
        return
    for row in entries:
        if isinstance(row, dict) and isinstance(row.get("report"), str):
            row["report"] = row["report"][:REPORT_CHARS]


def main() -> int:
    work = pathlib.Path(os.environ.get("RUN_DIR", "runs"))
    payload = verdict(work)
    trim(payload.get("history"))

    if not payload["transcript"]:
        print("::warning::no transcript was captured this run", file=sys.stderr)

    destination = pathlib.Path(os.environ.get("LOG_DIR", "log"))
    destination.mkdir(parents=True, exist_ok=True)
    name = f"{payload['identity'] or 'run'}-{payload['run_id'] or 'unknown'}.json"
    path = destination / name
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
