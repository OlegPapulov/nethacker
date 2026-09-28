"""Our loop: pull an elite, measure it, brief the operator, keep a winner.

The stock `nethackers evolve` is autonomous and its brief carries only scores,
so nothing this project has measured can reach the operator. This loop is the
same shape with one difference: **we compose the brief** from `experience.md`
and the baseline diagnosis, and hand that string to the project's mutator.

The mutator, the arena, the gate and the archive are all reused unchanged --
they are the parts that know about NetHack. Only the brief is ours.

    pull elite -> score it (published batch) -> build our brief
      -> operator edits the tree in the mutator
        -> smoke gate -> confirm on the published batch
          -> paired per-seed verdict -> keep or discard

The verdict is deliberately stricter than the project's, and the reason is in
`SCORING` in brief.py: progression takes ~5 distinct values across 15 seeds and
one seed can swing 0.18, so a positive mean is not evidence. We require most
seeds to improve.

Usage:
    evolve.py <identity> --iterations 2 --operator opencode2 \\
        --model opencode/big-pickle [--seed-mode pinned|hub|autoascend]
"""

from __future__ import annotations

import argparse
import datetime
import json
import random
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import brief as brief_mod  # noqa: E402

ARENA_IMAGE = (
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae"
)
MUTATOR_IMAGE = (
    "ghcr.io/dunnolab/nethackers-mutator@sha256:"
    "32c9222455b2f62082540a9f7293aa8fafc2bd5cb9ba7f4553fe79593706bee5"
)

#: Seeds kept for the paired comparison, from the arena's published batch.
PUBLISHED_SEEDS = 15

#: One cheap episode on a reserved seed, to reject a mutant that does not run.
SMOKE_SEED = 9000
SMOKE_STEPS = 2000

#: A win needs most seeds forward, and a floor in absolute terms. A 4-up-3-down
#: split is a coin flip under a sign test, so it is not a win.
MIN_SEEDS_FORWARD = 5
MIN_TWO_THIRDS = True


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def spec_for(identity: str, seeds: int = PUBLISHED_SEEDS, max_steps: int | None = None):
    from nethackers.contracts.models import ObjectiveSpec
    from nethackers.hub.objectives import CATALOG

    dev = CATALOG[identity]
    return ObjectiveSpec(
        name=f"{identity}__ours",
        kind="identity",
        batch=tuple((s, identity) for s in range(seeds)),
        max_steps=max_steps or dev.max_steps,
        no_progress_timeout=dev.no_progress_timeout,
        action_timeout_seconds=dev.action_timeout_seconds,
        aggregation=dev.aggregation,
    )


def score(tree: Path, identity: str, *, seeds: int = PUBLISHED_SEEDS, max_steps=None):
    from nethackers.harness import evaluate as E

    mean, evidence = E.evaluate(
        str(tree), spec_for(identity, seeds, max_steps), ARENA_IMAGE,
        now=now(), runtime="docker", max_parallel_evals=1,
    )
    results = [
        {
            "seed": r.trajectory_id, "turns": r.turns, "depth": r.max_depth,
            "progress": r.progress, "death": r.cause_of_death, "status": r.status,
        }
        for r in evidence.results
    ]
    return mean, results


def paired_verdict(child: list[dict], parent: list[dict]) -> dict:
    """Judge a mutant against its parent, per seed, on identical seeds."""
    child_by = {r["seed"]: r for r in child}
    parent_by = {r["seed"]: r for r in parent}
    shared = sorted(set(child_by) & set(parent_by))
    if not shared:
        return {"verdict": "NO-BASELINE", "why": "no shared seeds"}

    def moved(s):
        a, b = child_by[s], parent_by[s]
        return (
            abs(a["progress"] - b["progress"]) > 1e-9
            or a["turns"] != b["turns"]
            or a["depth"] != b["depth"]
        )

    def forward(s):
        a, b = child_by[s], parent_by[s]
        return (
            a["progress"] > b["progress"] + 1e-9
            or a["depth"] > b["depth"]
            or (a["depth"] == b["depth"] and a["turns"] > b["turns"])
        )

    changed = [s for s in shared if moved(s)]
    up = [s for s in changed if forward(s)]
    down = [s for s in changed if not forward(s)]
    deeper = [s for s in shared if child_by[s]["depth"] > parent_by[s]["depth"]]

    if not changed:
        verdict, why = "NOT-A-WIN", "no seed moved on any signal"
    elif len(up) < MIN_SEEDS_FORWARD:
        verdict, why = "NOT-A-WIN", (
            f"only {len(up)} seed(s) moved forward, below the {MIN_SEEDS_FORWARD} "
            f"required ({len(down)} went back)"
        )
    elif MIN_TWO_THIRDS and 3 * len(up) < 2 * len(changed):
        verdict, why = "NOT-A-WIN", (
            f"{len(up)} of {len(changed)} moved seeds went forward, short of "
            f"two-thirds ({len(down)} went back)"
        )
    else:
        verdict, why = "WIN", f"{len(up)} forward, {len(down)} back, {len(deeper)} deeper"

    return {
        "verdict": verdict, "why": why, "shared_seeds": len(shared),
        "changed": changed, "forward": up, "backward": down, "deeper": deeper,
    }


def fetch_seed(identity: str, mode: str, reference: str | None) -> Path:
    target = Path("seed-bot")
    if mode == "autoascend":
        import nethackers
        packaged = Path(nethackers.__file__).parent / "roots" / "autoascend"
        shutil.copytree(packaged, target)
    elif mode == "pinned" and reference:
        subprocess.run(["nethackers", "pull", reference, str(target)], check=True)
    else:
        elites = json.loads(
            subprocess.run(
                ["nethackers", "elites", "--scope", identity],
                capture_output=True, text=True, check=True,
            ).stdout
        )
        rows = [r for r in elites if r.get("identity") == identity]
        if not rows:
            raise SystemExit(f"no elite for {identity}")
        ref = rows[0]["reference"]
        subprocess.run(
            ["nethackers", "pull", f"{ref['repo']}@{ref['commit']}", str(target)],
            check=True,
        )
    if not (target / "bot.py").is_file():
        raise SystemExit("seed has no bot.py")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("identity")
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--operator", default="opencode2")
    parser.add_argument("--model", default="opencode/big-pickle")
    parser.add_argument("--seed-mode", default="hub", choices=["hub", "pinned", "autoascend"])
    parser.add_argument("--parent-ref")
    parser.add_argument("--workdir", default="runs")
    args = parser.parse_args()

    work = Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)

    print(f"=== {args.identity} · our loop · {args.iterations} iteration(s) ===", flush=True)
    parent = fetch_seed(args.identity, args.seed_mode, args.parent_ref)
    print(f"seed: {parent}", flush=True)

    parent_mean, parent_rows = score(parent, args.identity)
    print(f"seed baseline: {parent_mean:.4f} over {len(parent_rows)} seeds", flush=True)
    diagnosis = {
        "identity": args.identity, "mean_progress": parent_mean, "results": parent_rows,
    }
    (work / "baseline.json").write_text(json.dumps(diagnosis, indent=2))

    best_tree = parent
    best_mean = parent_mean
    best_rows = parent_rows
    history = []

    for iteration in range(1, args.iterations + 1):
        print(f"\n--- iteration {iteration} ---", flush=True)

        brief_text = brief_mod.build(
            args.identity,
            diagnosis,
            (REPO_ROOT / "experience.md").read_text(encoding="utf-8", errors="replace")
            if (REPO_ROOT / "experience.md").is_file() else "",
            (REPO_ROOT / "experiments.md").read_text(encoding="utf-8", errors="replace")
            if (REPO_ROOT / "experiments.md").is_file() else "",
        )
        (work / f"brief-{iteration}.md").write_text(brief_text)
        print(f"brief: {len(brief_text)} chars -> {work}/brief-{iteration}.md", flush=True)

        worktree = work / f"work-{iteration}"
        if worktree.exists():
            shutil.rmtree(worktree)
        shutil.copytree(best_tree, worktree)

        hypothesis = run_operator(worktree, brief_text, args)
        print(f"operator done; hypothesis: {hypothesis!r}", flush=True)

        smoke_mean, _ = score(
            worktree, args.identity, seeds=1, max_steps=SMOKE_STEPS
        )
        print(f"smoke: {smoke_mean:.4f}", flush=True)

        child_mean, child_rows = score(worktree, args.identity)
        verdict = paired_verdict(child_rows, best_rows)
        print(
            f"child {child_mean:.4f} vs parent {best_mean:.4f} -> {verdict['verdict']}: "
            f"{verdict['why']}",
            flush=True,
        )

        history.append({
            "iteration": iteration, "child_mean": child_mean,
            "parent_mean": best_mean, "hypothesis": hypothesis, **verdict,
        })
        (work / "history.json").write_text(json.dumps(history, indent=2))

        if verdict["verdict"] == "WIN":
            kept = work / f"winner-{iteration}"
            if kept.exists():
                shutil.rmtree(kept)
            shutil.copytree(worktree, kept)
            best_tree, best_mean, best_rows = kept, child_mean, child_rows
            print(f"KEPT as the new parent: {kept}", flush=True)

    print(f"\n=== done · {len(history)} iteration(s) ===")
    for entry in history:
        print(f"  {entry['iteration']}: {entry['verdict']:11} {entry['why']}")
    return 0


def run_operator(worktree: Path, brief_text: str, args) -> str | None:
    """Drive the project's mutator, passing OUR brief.

    Reuses `ContainerOperator`, so the sandbox caps, the platform args and the
    agent CLI are the project's, not ours. The only thing we change is the
    string handed to the agent.
    """
    from nethackers.harness.container_operator import ContainerOperator

    operator = ContainerOperator(
        harness=args.operator, image=MUTATOR_IMAGE, model=args.model,
    )
    result = operator.run(worktree, brief_text)
    usage = getattr(result, "usage", None)
    total = None
    if usage is not None:
        total = sum(
            int(getattr(usage, field, 0) or 0)
            for field in ("input", "output", "cache_creation", "cache_read")
        )
    print(
        f"  backend={getattr(result, 'backend', '?')} tokens={total} "
        f"stop={getattr(result, 'stopped_reason', '?')}",
        flush=True,
    )
    return extract_hypothesis(worktree)


_HYP = __import__("re").compile(r"#\s*hypothesis:\s*(.+)", __import__("re").IGNORECASE)


def extract_hypothesis(tree: Path) -> str | None:
    """Read the mutation's own `# hypothesis:` comment.

    The worktree is a copy of the parent, so it inherits every ancestor's
    comment. Only a line absent from the parent counts as this mutation's --
    the same rule the project's `_hypothesis_of` applies.
    """
    found: list[str] = []
    for path in sorted(tree.rglob("*.py")):
        try:
            found.extend(m.group(1).strip() for m in _HYP.finditer(path.read_text()))
        except (OSError, UnicodeDecodeError):
            continue
    return found[0] if found else None


if __name__ == "__main__":
    sys.exit(main())
