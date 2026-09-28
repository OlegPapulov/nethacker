import datetime
import json

from nethackers.contracts.models import ObjectiveSpec
from nethackers.harness import evaluate as E

IMAGE = (
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae"
)


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main() -> None:
    # One episode, serial, published seed 0. This is a liveness check, not a
    # score: the elite self-reports ~0.297 averaged over all 15 seeds, and a
    # single seed is worth far less. What matters is that the bot starts, plays
    # turns, and does not hit the 120 s startup guard.
    spec = ObjectiveSpec(
        name="probe",
        kind="identity",
        batch=((0, "val-dwa-law-fem"),),
        max_steps=20_000,
        no_progress_timeout=10_000,
        action_timeout_seconds=120.0,
        aggregation="mean",
    )
    mean, evidence = E.evaluate(
        ".", spec, IMAGE, now=now(), runtime="docker", max_parallel_evals=1
    )
    result = evidence.results[0]
    payload = {
        "mean_progress": mean,
        "status": result.status,
        "turns": result.turns,
        "max_depth": result.max_depth,
        "progress": result.progress,
        "milestone": result.milestone,
        "cause_of_death": result.cause_of_death,
        "error": (result.error or "")[:400],
        "wall_seconds": result.wall_seconds,
    }
    print("EPISODE " + json.dumps(payload), flush=True)
    with open("probe-result.json", "w") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
