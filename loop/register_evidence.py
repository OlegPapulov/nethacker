"""Build evidence in the exact shape `nethackers register --evidence` accepts.

`nethackers register` consumes one file and nothing else, and the hub is
strict about it: a payload missing `objective`, `evaluator_image`, `tier`,
`solution_digest` or `created_at` is a 500, even when the per-episode rows
already match. Those five are the whole reason this module exists rather than
a three-line `json.dump` at the call site.

`results` must be the RAW episode rows (`EpisodeResult.__dict__`), not the
loop's own projection. `score()` narrows each episode to seed/turns/depth/
progress/death/status for its paired arithmetic, and the hub reads
`trajectory_id`, `max_depth`, `cause_of_death` and `ascended` by name. Feeding
it the projection would register a payload whose episodes the hub cannot read,
which is the same class of silent no-op as registering with `--offline` set.

`confirm_score.py` is the reference implementation of this shape and is what
produced both published programs. It stays the source of truth: if the hub
ever grows a sixth required field, this and `confirm_score.py` must change
together.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

#: Self-reported is the only tier the client can produce unattended. Verified
#: runs live on Private Dungeons and are a hub-side path the loop cannot reach.
TIER = "self-reported"


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def build_payload(
    tree: Path, identity: str, mean: float, results: list[dict], arena_image: str
) -> dict:
    """The `register`-ready payload for `tree` scored on `identity`'s batch.

    `mean` and `results` come straight from the loop's own `score()`, so this
    registers exactly the number the loop judged on -- the loop never rescores
    on the way out, which would mean trusting a second sample of a batch whose
    per-seed SD is 0.033.
    """
    from nethackers.eval.runner import _solution_digest
    from nethackers.hub.objectives import CATALOG

    dev = CATALOG[identity]
    return {
        "solution_digest": _solution_digest(Path(tree)),
        "objective": {
            "character": None,
            "max_steps": dev.max_steps,
            "no_progress_timeout": dev.no_progress_timeout,
            "action_timeout_seconds": dev.action_timeout_seconds,
            "seed_set": identity,
        },
        "evaluator_image": arena_image,
        "tier": TIER,
        "episodes": len(results),
        "mean_progress": mean,
        "ascensions": sum(1 for r in results if r.get("ascended")),
        "created_at": now(),
        "results": results,
    }


def write_payload(payload: dict, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str))
    return path
