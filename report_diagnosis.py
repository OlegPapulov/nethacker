"""Render a diagnosis.json as a fixed-width table for the run summary.

Kept as a file rather than a heredoc inside the workflow's ``run: |`` block. A
heredoc nested there has to be indented to the block's own level, and getting
that wrong produces a step that fails silently with an empty log -- which is
exactly what happened twice in E11.

Usage: report_diagnosis.py <diagnosis.json>
"""

from __future__ import annotations

import json
import sys

HEADER = f"{'seed':>5} {'status':<10} {'turns':>7} {'depth':>6} {'prog':>7}  death"


def table(rows: list[dict]) -> str:
    lines = []
    for row in rows:
        death = row.get("death") or "-"
        lines.append(
            f"{row['seed']:>5} {row['status']:<10} {row['turns']:>7} "
            f"{row['depth']:>6} {row['progress']:>7}  {death}"
        )
    return "\n".join(lines)


def main() -> None:
    data = json.load(open(sys.argv[1]))
    print(f"tree:    {data.get('tree')}")
    print(f"identity: {data.get('identity')}")
    print()
    print(f"published mean:  {data.get('published_mean'):.4f}")
    print(f"validation mean: {data.get('validation_mean'):.4f}")
    print()
    print(f"turn-1 deaths: published {data.get('turn1_published')}, "
          f"validation {data.get('turn1_validation')}")
    print()
    print("### published (seeds 0-14)")
    print("```")
    print(HEADER)
    print(table(data.get("published", [])))
    print("```")
    print()
    print("### validation (seeds 1000+)")
    print("```")
    print(HEADER)
    print(table(data.get("validation", [])))
    print("```")

    # The conclusion this diagnostic exists to reach, stated in the log so it
    # cannot be skimmed past.
    died = (data.get("turn1_published") or 0) + (data.get("turn1_validation") or 0)
    if died:
        print()
        print(f"VERDICT baseline itself dies at turn 1 on {died} episode(s): "
              "a 0.0 from a mutant is NOT evidence the mutant is broken.")
    else:
        print()
        print("VERDICT baseline never dies at turn 1, so a turn-1 mutant is a "
              "real regression in the mutation.")


if __name__ == "__main__":
    main()
