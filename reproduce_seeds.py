"""Score ONE tree twice, in the same process, and report which seeds differ.

Why
---
N2' turned up a contradiction: two measurements of the same commit on the same
15 seeds gave 0.0995 and 0.1121. Rounding explained most of it, but seed 8
genuinely differed -- 21,384 turns at dlvl 19 in one run, 21,830 at dlvl 27 in
the other -- and that single seed accounted for the entire gap (0.1889 / 15 =
0.0126, exactly the observed difference).

So the arena is *not* fully deterministic, and "moved" and "noisy" are not the
same thing. Until the unstable seeds are known, the paired gate cannot tell a
real change from one.

This scores the same tree twice, back to back, in one process: same image, same
machine, same interpreter, nothing changed in between. Any seed that differs is
unstable, and no further measurement should be trusted on it.

Emits the per-seed table plus an `unstable_seeds` list, which
``report_confirm.py`` can consume to exclude those seeds from a verdict.

Usage: reproduce_seeds.py <tree> <identity> <out.json> [repeats]
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

from nethackers.contracts.models import ObjectiveSpec
from nethackers.hub.objectives import CATALOG
from nethackers.harness import evaluate as E

ARENA_IMAGE = (
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae"
)

# Two runs differing by more than this on progress is a real divergence, not
# float noise. The values are BALROG progression in [0, 1] and every distinct
# value seen in practice is separated by >= 0.01, so 1e-6 is unambiguous.
PROGRESS_EPS = 1e-6


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def spec_for(identity: str) -> ObjectiveSpec:
    dev = CATALOG[identity]
    return ObjectiveSpec(
        name=f"{identity}__reproduce",
        kind="identity",
        batch=tuple((seed, identity) for seed in range(15)),
        max_steps=dev.max_steps,
        no_progress_timeout=dev.no_progress_timeout,
        action_timeout_seconds=dev.action_timeout_seconds,
        aggregation=dev.aggregation,
    )


def main() -> None:
    tree, identity, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    repeats = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    spec = spec_for(identity)

    runs: list[dict[int, dict]] = []
    for attempt in range(repeats):
        print(f"== repeat {attempt + 1}/{repeats} ==", flush=True)
        mean, evidence = E.evaluate(tree, spec, ARENA_IMAGE, now=now(), runtime="docker")
        rows = {r.trajectory_id: r for r in evidence.results}
        runs.append(rows)
        print(f"  mean {mean:.4f}", flush=True)
        unstable_here = []
        if attempt:
            first = runs[0]
            for seed in sorted(rows):
                a, b = first[seed], rows[seed]
                if (
                    a.turns != b.turns
                    or a.max_depth != b.max_depth
                    or abs(a.progress - b.progress) > PROGRESS_EPS
                ):
                    unstable_here.append(seed)
        if attempt:
            print(f"  seeds differing from repeat 1: {unstable_here}", flush=True)

    # A seed is unstable if ANY pair of repeats disagrees.
    unstable: set[int] = set()
    for seed in sorted(runs[0]):
        reference = runs[0][seed]
        for other in runs[1:]:
            candidate = other[seed]
            if (
                reference.turns != candidate.turns
                or reference.max_depth != candidate.max_depth
                or abs(reference.progress - candidate.progress) > PROGRESS_EPS
            ):
                unstable.add(seed)

    stable = sorted(set(runs[0]) - unstable)
    print()
    print("== reproducibility ==")
    print(f"  seeds tested        {len(runs[0])}")
    print(f"  stable              {len(stable)}  {stable}")
    print(f"  UNSTABLE            {len(unstable)}  {sorted(unstable)}")
    if unstable:
        print()
        print("  per-seed divergence:")
        for seed in sorted(unstable):
            a, b = runs[0][seed], runs[1][seed]
            print(
                f"    seed {seed:>2}: {a.turns:>6}t dlvl {a.max_depth:>2} "
                f"{a.progress:.4f}  ->  {b.turns:>6}t dlvl {b.max_depth:>2} "
                f"{b.progress:.4f}   ({a.cause_of_death} -> {b.cause_of_death})"
            )

    payload = {
        "tree": str(tree),
        "identity": identity,
        "repeats": repeats,
        "stable_seeds": stable,
        "unstable_seeds": sorted(unstable),
        "runs": [
            {
                "mean_progress": sum(r.progress for r in rows.values()) / len(rows),
                "results": [r.__dict__ for r in rows.values()],
            }
            for rows in runs
        ],
    }
    with open(out_path, "w") as handle:
        json.dump(payload, handle, indent=2, default=str)
    print()
    print(f"STABLE_SEEDS {stable}")
    print(f"UNSTABLE_SEEDS {sorted(unstable)}")


if __name__ == "__main__":
    main()
