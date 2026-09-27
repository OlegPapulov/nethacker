"""Report a confirm run, and compare it with the score the loop claimed.

A run's `dev_fitness` is what `evolve` believed. This re-scores the same tree
from a clean checkout, so the two can be compared. If they disagree materially
the claimed number came from a different tree than the one being published, and
that must be resolved before registering anything.

Usage: report_confirm.py <evidence.json> <expected-or-0>
"""

from __future__ import annotations

import json
import sys

# Beyond this, treat the claim and the re-score as different trees rather than
# as noise. Both numbers are means over the same 15 seeds, so ordinary
# run-to-run spread should be far smaller; AutoAscend-family bots are
# deterministic given a seed, but a difference this large means the artifact
# is not the artifact.
MATERIAL_GAP = 0.02


def main() -> None:
    data = json.load(open(sys.argv[1]))
    expected = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

    mean = data["mean_progress"]
    results = data["results"]

    print(f"tree:      {data.get('tree')}")
    print(f"identity:  {data.get('identity')}")
    print(f"episodes:  {data.get('episodes')}   ascensions: {data.get('ascensions')}")
    print(f"CONFIRMED  {mean:.4f}")
    print()

    turns = [r["turns"] for r in results]
    depths = [r["max_depth"] for r in results]
    print(f"turns  min {min(turns)}  mean {sum(turns) // len(turns)}  max {max(turns)}")
    print(f"depth  min {min(depths)}  max {max(depths)}")
    print()

    if expected > 0:
        delta = mean - expected
        verdict = "MATCH" if abs(delta) <= MATERIAL_GAP else "MISMATCH"
        print(f"claimed by the run: {expected:.4f}")
        print(f"delta:              {delta:+.4f}  ->  {verdict}")
        if verdict == "MISMATCH":
            print()
            print("These differ by more than the same-seed spread, so the tree being")
            print("scored is probably not the tree the run evaluated. Do not register")
            print("it on the strength of the claimed number; re-derive the tree from")
            print("the run's own work directory instead.")
    else:
        print("(no expected score supplied; nothing compared)")

    print()
    print("per-seed:")
    for r in sorted(results, key=lambda r: r["trajectory_id"]):
        print(
            f"  {r['trajectory_id']:>2}  {r['status']:<9} {r['turns']:>6} turns  "
            f"dlvl {r['max_depth']:>2}  {r['progress']:.4f}  "
            f"{r.get('cause_of_death') or '-'}"
        )


if __name__ == "__main__":
    main()
