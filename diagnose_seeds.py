"""Score one bot tree on both seed tiers, to see whether a bad run is the bot
or the seeds.

E11's mutant reported ``progress=0.000 completed turns=1`` with a
``uint8`` underflow on ``tty_cursor[0] - 1``. That expression is the
``tty_chars`` -> ``chars`` row offset, so it is probably *pre-existing*
AutoAscend code rather than anything the agent wrote. This script decides
that, cheaply and without an agent:

* the **published** batch, seeds 0-14, which the hub scores;
* the **validation** batch, seeds 1000+, which the loop may see but the
  published batch does not cover.

If the *unmodified* tree also dies at turn 1 on either tier, then a 0.0 says
nothing about the mutant and any prescreen built on it is selecting on noise.
If it dies on one tier and not the other, the fault is seed-specific and worth
knowing about, because the prescreen reads the validation tier while the
registerable number comes from the published one.

Usage: diagnose_seeds.py <tree-dir> <identity> <out.json> [n_per_tier]
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

from nethackers.harness import evaluate as E
from nethackers.harness.seeds import validation_spec

ARENA_IMAGE = (
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae"
)

PUBLISHED_SEEDS = 15


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def rows(evidence) -> list[dict]:
    """Per-seed shape, kept small: turn count is the signal, not the score.

    ``progress`` is kept at FULL precision. Rounding it to 4dp made two runs of
    the same commit look different on all 15 seeds, which cost a real
    investigation: turns and depth matched exactly and only the display was
    rounded, so a 1e-5 residual read as a discrepancy. Display rounding
    belongs in the report, never in the data.
    """
    return [
        {
            "seed": r.trajectory_id,
            "status": r.status,
            "turns": r.turns,
            "depth": r.max_depth,
            "progress": r.progress,
            "milestone": r.milestone,
            "death": r.cause_of_death,
            "error": (r.error or "")[:160],
        }
        for r in evidence.results
    ]


def main() -> None:
    tree, identity, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 5

    published = Path(f"diag-published-{identity}.json")
    validation = Path(f"diag-validation-{identity}.json")

    print(f"== published batch (seeds 0-{PUBLISHED_SEEDS - 1}) ==", flush=True)
    mean_pub, ev_pub = E.evaluate(
        tree,
        validation_spec(identity, n=PUBLISHED_SEEDS, start=0),
        ARENA_IMAGE,
        now=now(),
        runtime="docker",
    )
    json.dump(rows(ev_pub), published.open("w"), indent=2)
    print(f"PUBLISHED_MEAN {mean_pub:.4f}", flush=True)

    print(f"== validation batch (seeds 1000-{1000 + n - 1}) ==", flush=True)
    mean_val, ev_val = E.evaluate(
        tree,
        validation_spec(identity, n=n, start=1000),
        ARENA_IMAGE,
        now=now(),
        runtime="docker",
    )
    json.dump(rows(ev_val), validation.open("w"), indent=2)
    print(f"VALIDATION_MEAN {mean_val:.4f}", flush=True)

    dead_pub = [r for r in rows(ev_pub) if r["turns"] <= 1]
    dead_val = [r for r in rows(ev_val) if r["turns"] <= 1]
    print(f"TURN1_PUBLISHED {len(dead_pub)}/{len(ev_pub.results)}", flush=True)
    print(f"TURN1_VALIDATION {len(dead_val)}/{len(ev_val.results)}", flush=True)

    payload = {
        "tree": str(tree),
        "identity": identity,
        "published_mean": mean_pub,
        "validation_mean": mean_val,
        "turn1_published": len(dead_pub),
        "turn1_validation": len(dead_val),
        "published": rows(ev_pub),
        "validation": rows(ev_val),
    }
    json.dump(payload, open(out_path, "w"), indent=2, default=str)
    # A non-zero exit would fail the workflow step; this is a report, not a gate.
    print("DIAG_COMPLETE", flush=True)


if __name__ == "__main__":
    main()
