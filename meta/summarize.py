"""Print the committed run record, for checking a prediction after a run.

`meta/experiments.md` holds one entry per change to the brief, each with a
falsifiable prediction. Checking a prediction means reading the run's own
committed numbers, and those live in `log/<identity>-<runid>.json` --
`log_verdict.py` writes them, and the workflow commits them. This is the
read-only view of that, so a prediction can be settled without pulling a
transcript out of an artifact.

Read-only by construction: it opens nothing for writing, imports only the
standard library, and takes no arguments that change behaviour. It exists to be
run while reading a diff, not to become a dependency of the loop.

    python meta/summarize.py                  # every run
    python meta/summarize.py 36710578461      # one run, in full

The derived columns are the ones worth watching. `self-reverted` is the
behaviour the "do not revert your own change" instruction targets: it greps the
agent's own report for a claim of reverting, and it is the number that moved
when that instruction landed. A `self-reverted` iteration is not necessarily
wrong -- reverting a measured regression is right, and run 36710578461 did
exactly that -- so the column is a prompt to read the report, not a score.
"""

from __future__ import annotations

import json
import pathlib
import sys

#: Columns wide enough for the header and its values.
COLUMNS = ("run", "it", "verdict", "child", "parent", "delta", "fwd", "back", "reverted")


def log_dir() -> pathlib.Path:
    return pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "log")


def load() -> list[dict]:
    """Every run record, oldest first. Unparseable files are skipped, not fatal:
    a half-written log from a killed job should not hide the runs that worked."""
    out: list[dict] = []
    for path in sorted(log_dir().glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"::warning::skipping {path.name}: {exc}", file=sys.stderr)
            continue
        if isinstance(payload, dict):
            out.append(payload)
    return out


def _cell(value, width: int) -> str:
    return str(value).ljust(width)


def _table(rows: list[list[str]], headers: tuple[str, ...]) -> str:
    widths = [
        max(len(headers[i]), max((len(r[i]) for r in rows), default=0))
        for i in range(len(headers))
    ]
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    out = [line, "  ".join("-" * w for w in widths)]
    for row in rows:
        out.append("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
    return "\n".join(out)


def summarise(payload: dict) -> list[str] | None:
    """One row per iteration, or None for a run that recorded no history."""
    identity = payload.get("identity") or "?"
    rows: list[list[str]] = []
    for entry in payload.get("history") or []:
        if not isinstance(entry, dict):
            continue
        child = entry.get("child_mean")
        parent = entry.get("parent_mean")
        delta = (
            f"{child - parent:+.4f}"
            if isinstance(child, (int, float)) and isinstance(parent, (int, float))
            else "?"
        )
        report = entry.get("report") or ""
        low = report.lower()
        reverted = "yes" if "revert" in low else "-"
        rows.append([
            str(payload.get("run_id") or "?"),
            str(entry.get("iteration", "?")),
            str(entry.get("verdict") or "?"),
            f"{child:.4f}" if isinstance(child, (int, float)) else "?",
            f"{parent:.4f}" if isinstance(parent, (int, float)) else "?",
            delta,
            str(len(entry.get("forward") or [])),
            str(len(entry.get("backward") or [])),
            reverted,
        ])
    if not rows:
        return None
    header = f"\n### {identity}  run {rows[0][0]}"
    return header + "\n" + _table(rows, COLUMNS)


def detail(payload: dict) -> None:
    """One run in full: the agent's own words, which is where the reasoning is."""
    print(f"\n=== {payload.get('identity')} run {payload.get('run_id')} ===")
    print(f"operator: {payload.get('operator')} / {payload.get('model')}")
    print(f"conclusion: {payload.get('conclusion')}   transcript: {payload.get('transcript')}")
    for entry in payload.get("history") or []:
        if not isinstance(entry, dict):
            continue
        print(f"\n--- iteration {entry.get('iteration')}: "
              f"{entry.get('verdict')} ({entry.get('why')})")
        print(f"hypothesis [{entry.get('hypothesis_source')}]: "
              f"{entry.get('hypothesis')}")
        if entry.get("report"):
            print(f"\nreport:\n{entry['report']}")
        if entry.get("publish"):
            print(f"\npublish: {json.dumps(entry['publish'], indent=2)}")
    baseline = payload.get("baseline") or {}
    if baseline:
        print(f"\nbaseline mean: {baseline.get('mean_progress')}")
        for row in baseline.get("results") or []:
            print(f"  seed {row.get('seed')}: progress={row.get('progress'):.4f} "
                  f"turns={row.get('turns')} depth={row.get('depth')} "
                  f"death={row.get('death')}")


def main(argv: list[str]) -> int:
    runs = load()
    if not runs:
        print(f"no run records in {log_dir()}/", file=sys.stderr)
        return 1
    if len(argv) > 1 and argv[1] != "-":
        wanted = [r for r in runs if str(r.get("run_id")) == argv[1]]
        if not wanted:
            print(f"no run {argv[1]}; have "
                  f"{', '.join(str(r.get('run_id')) for r in runs)}", file=sys.stderr)
            return 1
        for payload in wanted:
            detail(payload)
        return 0
    for payload in runs:
        text = summarise(payload)
        if text:
            print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
