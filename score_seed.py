"""Score one bot tree on the published 15-seed batch for a single identity.

This is the `confirm` tier of the two-stage evaluation in
`loop/prescreen.py`: the published seeds 0-14, the pinned arena image, the
limits the hub itself uses (`max_steps=1_000_000`, `no_progress_timeout=10_000`,
`action_timeout=120s`). A number produced here is comparable with everyone
else's on the board and is the only kind that may be registered.

Writes `seed-eval.json` next to the tree and prints `SEED_SCORE <mean>`, so a
caller can grep the log without parsing JSON.

Usage: score_seed.py <tree-dir> <identity> <out.json>
"""

from __future__ import annotations

import datetime
import json
import sys

from nethackers.contracts.models import ObjectiveSpec
from nethackers.harness import evaluate as E

ARENA_IMAGE = (
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae"
)

# The published batch: trajectory ids 0-14, the seeds the hub scores.
PUBLISHED_SEEDS = 15


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main() -> None:
    tree, identity, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = ObjectiveSpec(
        name=f"{identity}__seed",
        kind="identity",
        batch=tuple((seed, identity) for seed in range(PUBLISHED_SEEDS)),
        max_steps=1_000_000,
        no_progress_timeout=10_000,
        action_timeout_seconds=120.0,
        aggregation="mean",
    )
    mean, evidence = E.evaluate(tree, spec, ARENA_IMAGE, now=now(), runtime="docker")
    payload = {
        "identity": identity,
        "tree": tree,
        "seed_mean_progress": mean,
        "results": [result.__dict__ for result in evidence.results],
    }
    with open(out_path, "w") as handle:
        json.dump(payload, handle, default=str)
    print(f"SEED_SCORE {mean:.4f}")


if __name__ == "__main__":
    main()
