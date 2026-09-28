"""Run the traced bot over an identity's published seeds.

Thin wrapper around ``nethackers.harness.evaluate`` that points
``NETHACK_TRACE_DIR`` somewhere useful and then lets the arena do the work. The
arena gives each episode its own process; the bot writes one JSON file per
episode into that directory, and ``classify_deaths.py`` reads them afterwards.

Nothing here interprets the results. Keeping the run and the analysis apart
means the classifier can be re-run against a stored trace set without paying for
another 15-episode batch.

Usage: run_traced.py <identity> [n-seeds]
"""

from __future__ import annotations

import datetime
import os
import sys
from pathlib import Path

from nethackers.contracts.models import ObjectiveSpec
from nethackers.hub.objectives import CATALOG
from nethackers.harness import evaluate as E

ARENA_IMAGE = os.environ.get(
    "ARENA_IMAGE",
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae",
)

#: Episodes share a workdir, so each gets its own subdirectory to keep the
#: per-episode trace files apart.
PER_EPISODE_DIR = True


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main() -> None:
    identity = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    dev = CATALOG[identity]
    seeds = list(range(min(count, len(dev.batch))))

    spec = ObjectiveSpec(
        name=f"{identity}__traced",
        kind="identity",
        batch=tuple((seed, identity) for seed in seeds),
        max_steps=dev.max_steps,
        no_progress_timeout=dev.no_progress_timeout,
        action_timeout_seconds=dev.action_timeout_seconds,
        aggregation=dev.aggregation,
    )

    print(f"tracing {identity} on seeds {seeds[0]}..{seeds[-1]}", flush=True)
    mean, evidence = E.evaluate(
        "./trace-bot",
        spec,
        ARENA_IMAGE,
        now=now(),
        runtime="docker",
        max_parallel_evals=1,
    )

    rows = [
        {
            "seed": r.trajectory_id,
            "status": r.status,
            "turns": r.turns,
            "depth": r.max_depth,
            "progress": r.progress,
            "death": r.cause_of_death,
            "error": (r.error or "")[:160],
        }
        for r in evidence.results
    ]
    Path("diagnosis.json").write_text(
        __import__("json").dumps(
            {
                "identity": identity,
                "mean_progress": mean,
                "seeds": len(seeds),
                "results": rows,
            },
            indent=2,
        )
    )
    print(f"MEAN {mean:.4f}")
    for row in sorted(rows, key=lambda r: r["turns"]):
        print(
            f"  {row['seed']:>2} {row['turns']:>6}t dl{row['depth']:>2} "
            f"{row['progress']:.4f}  {row['death'] or '-'}"
        )


if __name__ == "__main__":
    main()
