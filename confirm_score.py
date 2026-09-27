"""Score one solution tree on the published 15-seed batch for one identity.

This is the `confirm` tier: the same batch, the same pinned image and the same
limits the hub uses, so the number is directly comparable with every other row
on the board and is what may be registered.

Emits evidence in EXACTLY the shape `nethackers eval` produces, because
`nethackers register --evidence` consumes that and nothing else. The hub
returned a 500 when handed a file missing `objective`, `evaluator_image`,
`tier`, `solution_digest` or `created_at` -- so all five are required even
though the per-episode rows already match.

Pass a second tree and the same 15 seeds are played for both, which is how a
candidate is measured against its own parent on one runner rather than across
machines. Because a seed fully determines a game, the two sets of per-seed rows
can be compared pairwise -- a far tighter test than comparing two means.

Usage:
    confirm_score.py <tree> <identity> <out.json> [<parent-tree>]
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


def run(tree: str, spec: ObjectiveSpec) -> tuple[float, list[dict]]:
    mean, evidence = E.evaluate(tree, spec, ARENA_IMAGE, now=now(), runtime="docker")
    return mean, [r.__dict__ for r in evidence.results]


def report(label: str, mean: float, results: list[dict]) -> None:
    turns = [r["turns"] for r in results]
    depths = [r["max_depth"] for r in results]
    print(f"\n== {label} ==")
    print(f"  mean {mean:.4f}   turns min {min(turns)} mean {sum(turns) // len(turns)} "
          f"max {max(turns)}   depth max {max(depths)}")
    for r in sorted(results, key=lambda r: r["trajectory_id"]):
        print(f"   {r['trajectory_id']:>2}  {r['turns']:>6}  {r['max_depth']:>3}  "
              f"{r['progress']:.4f}  {r.get('cause_of_death') or '-'}")


def main() -> None:
    tree, identity, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    parent = sys.argv[4] if len(sys.argv) > 4 else None

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

    mean, results = run(tree, spec)
    report(f"candidate  {tree}", mean, results)

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
    print(f"\nCONFIRM_MEAN {mean:.4f}")
    print(f"DIGEST {payload['solution_digest']}")

    if not parent:
        return

    parent_mean, parent_results = run(parent, spec)
    report(f"parent     {parent}", parent_mean, parent_results)
    payload["parent"] = {
        "tree": parent,
        "digest": _solution_digest(Path(parent)),
        "mean_progress": parent_mean,
        "results": parent_results,
    }
    with open(out_path, "w") as handle:
        json.dump(payload, handle, indent=2, default=str)

    # Pairwise: the same seed is the same game, so per-seed differences isolate
    # the mutation's effect from seed luck.
    by_seed = {r["trajectory_id"]: r["progress"] for r in results}
    p_by_seed = {r["trajectory_id"]: r["progress"] for r in parent_results}
    deltas = [by_seed[s] - p_by_seed[s] for s in sorted(by_seed) if s in p_by_seed]
    wins = sum(1 for d in deltas if d > 1e-9)
    losses = sum(1 for d in deltas if d < -1e-9)
    better_depth = sum(
        1
        for r in results
        if r["max_depth"] > next(p["max_depth"] for p in parent_results
                                 if p["trajectory_id"] == r["trajectory_id"])
    )
    print("\n== paired comparison, same 15 seeds ==")
    print(f"  candidate mean {mean:.4f}   parent mean {parent_mean:.4f}   "
          f"delta {mean - parent_mean:+.4f}")
    print(f"  seeds improved {wins}   worsened {losses}   identical {len(deltas) - wins - losses}")
    print(f"  seeds reaching a deeper level: {better_depth}/{len(deltas)}")
    if deltas:
        mean_delta = sum(deltas) / len(deltas)
        print(f"  mean paired delta {mean_delta:+.4f}")


if __name__ == "__main__":
    main()
