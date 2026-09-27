"""Judge a confirm run, and decide whether it is fit to register.

Two independent questions, and conflating them is what produced a published
row that did not hold up:

1. **Does this tree score what the run claimed?** A run's ``dev_fitness`` is
   what ``evolve`` believed. Re-scoring the same tree from a clean checkout
   checks that. A large gap means the tree about to be published is not the
   tree the run evaluated.

2. **Is this tree actually better than its parent?** This is the question that
   matters, and a threshold on the *mean* cannot answer it. A seed fully
   determines a NetHack game, so when both trees are scored over the same 15
   seeds the comparison can be made pairwise -- and the paired result is far
   sharper than any difference of means.

   N1 is why. A candidate scoring 0.5023 against a parent at 0.5054 looks like
   a rounding difference, and a 0.02 threshold on the mean waved it through.
   The paired view was unambiguous: **0 seeds improved, 1 worsened, 14
   identical.** Fourteen bit-identical results means the mutation barely fires
   on this batch, and the entire apparent delta lived in one seed.

So the verdict is driven by the paired counts when a parent was scored, and by
the claimed-vs-rescored gap when one was not. Anything short of a win exits
non-zero so a workflow step can refuse to publish.

Usage:
    report_confirm.py <evidence.json> [expected]
"""

from __future__ import annotations

import json
import sys

# --- claim vs re-score -------------------------------------------------------
# Both are means over the same 15 seeds of a deterministic-given-seed game, so
# ordinary spread should be very small. Beyond this the two numbers describe
# different trees. N1 saw 0.0059 between two runs of the *same* tree, so the
# threshold sits above that: it is a "these are not the same artifact" alarm,
# not a noise allowance.
MATERIAL_GAP = 0.02

# --- paired verdict ----------------------------------------------------------
# A candidate must improve at least this many seeds, and must not be net
# negative. One improved seed out of fifteen is indistinguishable from a coin
# flip; three is the smallest count that carries any information at all.
MIN_SEEDS_IMPROVED = 3


def paired_verdict(data: dict) -> tuple[str, str] | None:
    """Compare candidate and parent seed-by-seed. None when no parent was scored."""
    parent = data.get("parent")
    if not parent:
        return None

    mine = {r["trajectory_id"]: r for r in data["results"]}
    theirs = {r["trajectory_id"]: r for r in parent["results"]}
    shared = sorted(set(mine) & set(theirs))

    improved = [s for s in shared if mine[s]["progress"] > theirs[s]["progress"] + 1e-9]
    worsened = [s for s in shared if mine[s]["progress"] < theirs[s]["progress"] - 1e-9]
    identical = [s for s in shared if abs(mine[s]["progress"] - theirs[s]["progress"]) <= 1e-9]
    deeper = [
        s
        for s in shared
        if mine[s]["max_depth"] > theirs[s]["max_depth"]
    ]

    delta = data["mean_progress"] - parent["mean_progress"]
    lines = [
        f"  seeds improved {len(improved)}  worsened {len(worsened)}  "
        f"identical {len(identical)}   (of {len(shared)})",
        f"  seeds reaching a deeper level: {len(deeper)}/{len(shared)}",
        f"  mean delta {delta:+.4f}",
    ]
    if identical and len(identical) >= len(shared) - 1:
        lines.append(
            f"  {len(identical)} of {len(shared)} seeds are bit-identical: the "
            "change barely fires on this batch, and the whole delta lives in "
            "the seeds that differ."
        )
    if improved:
        lines.append(f"  improved seeds: {improved}")
    if worsened:
        lines.append(f"  worsened seeds: {worsened}")

    if len(improved) == 0:
        verdict = "NOT-A-WIN"
        why = "no seed improved"
    elif len(improved) < MIN_SEEDS_IMPROVED:
        verdict = "NOT-A-WIN"
        why = (
            f"only {len(improved)} seed(s) improved, below the "
            f"{MIN_SEEDS_IMPROVED} needed to distinguish a real effect from a "
            "coin flip"
        )
    elif len(worsened) > len(improved):
        verdict = "NOT-A-WIN"
        why = f"more seeds worsened ({len(worsened)}) than improved ({len(improved)})"
    elif delta <= 0:
        verdict = "NOT-A-WIN"
        why = f"mean delta is {delta:+.4f}, not positive"
    else:
        verdict = "WIN"
        why = f"{len(improved)} seeds improved, mean {delta:+.4f}"

    return verdict, "\n".join([f"  {why}", *lines])


def main() -> None:
    data = json.load(open(sys.argv[1]))
    expected = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

    mean = data["mean_progress"]
    results = data["results"]
    objective = data.get("objective") or {}

    print(f"digest:    {data.get('solution_digest')}")
    print(f"tier:      {data.get('tier')}")
    print(f"image:     {str(data.get('evaluator_image'))[:48]}...")
    print(f"seed_set:  {objective.get('seed_set')}")
    print(f"episodes:  {data.get('episodes')}   ascensions: {data.get('ascensions')}")
    print(f"RESCORED   {mean:.4f}")

    turns = [r["turns"] for r in results]
    depths = [r["max_depth"] for r in results]
    print(f"turns  min {min(turns)}  mean {sum(turns) // len(turns)}  max {max(turns)}")
    print(f"depth  min {min(depths)}  max {max(depths)}")

    verdict = "UNVERIFIED"

    print()
    print("== claim vs re-score ==")
    if expected > 0:
        gap = mean - expected
        same = abs(gap) <= MATERIAL_GAP
        print(f"  claimed by the run: {expected:.4f}")
        print(f"  re-scored here:     {mean:.4f}")
        print(f"  gap {gap:+.4f}  ->  {'MATCH' if same else 'MISMATCH'}")
        if not same:
            print("  these describe different trees; do not register on the claim")
    else:
        print("  (no claimed score supplied)")

    print()
    print("== paired against parent ==")
    paired = paired_verdict(data)
    if paired is None:
        print("  (no parent scored; nothing to compare)")
        verdict = "UNVERIFIED"
    else:
        verdict, detail = paired
        print(detail)
        print(f"  VERDICT {verdict}")

    print()
    print("per-seed:")
    for r in sorted(results, key=lambda r: r["trajectory_id"]):
        print(
            f"  {r['trajectory_id']:>2}  {r['status']:<9} {r['turns']:>6} turns  "
            f"dlvl {r['max_depth']:>2}  {r['progress']:.4f}  "
            f"{r.get('cause_of_death') or '-'}"
        )

    print()
    print(f"REGISTERABLE {'yes' if verdict == 'WIN' else 'no'}  (verdict {verdict})")

    # Non-zero when the tree must not be published, so a workflow step can gate
    # on it rather than on a human reading the log.
    raise SystemExit(0 if verdict == "WIN" else 1)


if __name__ == "__main__":
    main()
