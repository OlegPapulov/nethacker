"""Score a solution tree on the published 15-seed batch for one identity.

This is the `confirm` tier: the same batch, the same pinned image and the same
limits the hub uses, so the number is directly comparable with every other row
on the board and is what may be registered.

Emits evidence in EXACTLY the shape `nethackers eval` produces, because
`nethackers register --evidence` consumes that and nothing else. The hub
returned a 500 when handed a file missing `objective`, `evaluator_image`,
`tier`, `solution_digest` or `created_at` -- so all five are required even
though the per-episode rows already match.

Usage: confirm_score.py <tree-dir> <identity> <out.json>
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

from nethackers.contracts.models import ObjectiveSpec
from nethackers.eval.runner import _solution_digest
from nethackers.hub.objectives import CATALOG
from nethackers.harness import evaluate as E

ARENA_IMAGE = (
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae"
)
TIER = "self-reported"


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main() -> None:
    tree, identity, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    dev = CATALOG[identity]
    spec = ObjectiveSpec(
        name=f"{identity}__confirm",
        kind="identity",
        batch=tuple((seed, identity) for seed in range(15)),
        max_steps=dev.max_steps,
        no_progress_timeout=dev.no_progress_timeout,
        action_timeout_seconds=dev.action_timeout_seconds,
        aggregation=dev.aggregation,
    )
    mean, evidence = E.evaluate(tree, spec, ARENA_IMAGE, now=now(), runtime="docker")
    results = [r.__dict__ for r in evidence.results]

    # Same five top-level keys `nethackers eval` writes. The hub validates the
    # envelope, not just the rows.
    payload = {
        "solution_digest": _solution_digest(Path(tree)),
        "objective": {
            "character": None,
            "max_steps": dev.max_steps,
            "no_progress_timeout": dev.no_progress_timeout,
            "action_timeout_seconds": dev.action_timeout_seconds,
            "seed_set": identity,
        },
        "evaluator_image": ARENA_IMAGE,
        "tier": TIER,
        "episodes": len(results),
        "mean_progress": mean,
        "ascensions": sum(1 for r in results if r.get("ascended")),
        "created_at": now(),
        "results": results,
    }
    with open(out_path, "w") as handle:
        json.dump(payload, handle, indent=2, default=str)

    print(f"CONFIRM_MEAN {mean:.4f}")
    print(f"EPISODES {len(results)}")
    print(f"DIGEST {payload['solution_digest']}")
    print("per-seed (seed, turns, depth, progress, death):")
    for r in sorted(results, key=lambda r: r["trajectory_id"]):
        print(
            f"  {r['trajectory_id']:>2}  {r['turns']:>6}  {r['max_depth']:>3}  "
            f"{r['progress']:.4f}  {r.get('cause_of_death') or '-'}"
        )


if __name__ == "__main__":
    main()
