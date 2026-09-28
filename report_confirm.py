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

**Unstable seeds are excluded.** Not every seed is reproducible. The
``reproduce`` workflow scores one tree repeatedly and finds the seeds that
disagree between runs -- long games in particular. N2' found one where the same
commit produced 21,384 turns at dlvl 19 in one run and 21,830 at dlvl 27 in the
next, and that single seed moved a 15-seed mean by 0.0126. Counting such a seed
as evidence that a mutation "did something" is counting noise, so
``--stable-from`` drops those seeds from the verdict entirely.

So the verdict is driven by the paired counts when a parent was scored, and by
the claimed-vs-rescored gap when one was not. Anything short of a win exits
non-zero so a workflow step can refuse to publish.

Usage:
    report_confirm.py <evidence.json> [expected] [--stable-from repro.json]
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
# A candidate must move at least this many seeds on ANY observable signal, and
# the movement must be positive.
#
# N3a is why this counts turns and depth and not just progression. Over 15
# seeds the progression metric takes only FIVE distinct values, because BALROG
# progression pins to milestone plateaus, so its SE of the mean is 0.0281 --
# larger than any single change this loop produces. Turns takes 15 distinct
# values and is near-continuous, and it resolved a seed progression missed
# entirely. A gate on progression alone is therefore close to unreachable for a
# genuine single change, and would either pass noise or reject everything.
MIN_SEEDS_MOVED = 3


def paired_verdict(data: dict, stable: set[int] | None = None) -> tuple[str, str] | None:
    """Compare candidate and parent seed-by-seed. None when no parent was scored.

    "Moved" means turns or depth or progression changed at all -- the count of
    seeds the mutation actually reached. "Improved" is the subset where the
    movement was in the right direction. A real change moves many seeds; a no-op
    moves one or two, which is what the petrify-guard change did.
    """
    parent = data.get("parent")
    if not parent:
        return None

    mine = {r["trajectory_id"]: r for r in data["results"]}
    theirs = {r["trajectory_id"]: r for r in parent["results"]}
    shared = sorted(set(mine) & set(theirs))
    dropped = []
    if stable is not None:
        dropped = [s for s in shared if s not in stable]
        shared = [s for s in shared if s in stable]
        if not shared:
            return "UNVERIFIED", (
                "  no stable seeds remain: every seed in this batch was "
                "unstable under repeated scoring, so nothing can be measured"
            )

    def moved(s: int) -> bool:
        a, b = mine[s], theirs[s]
        return (
            abs(a["progress"] - b["progress"]) > 1e-9
            or a["turns"] != b["turns"]
            or a["max_depth"] != b["max_depth"]
        )

    def forward(s: int) -> bool:
        a, b = mine[s], theirs[s]
        return (
            a["progress"] > b["progress"] + 1e-9
            or a["max_depth"] > b["max_depth"]
            or (a["max_depth"] == b["max_depth"] and a["turns"] > b["turns"])
        )

    changed = [s for s in shared if moved(s)]
    improved = [s for s in changed if forward(s)]
    regressed = [s for s in changed if not forward(s)]
    still = [s for s in shared if not moved(s)]
    prog_up = [s for s in shared if mine[s]["progress"] > theirs[s]["progress"] + 1e-9]
    prog_down = [s for s in shared if mine[s]["progress"] < theirs[s]["progress"] - 1e-9]
    deeper = [s for s in shared if mine[s]["max_depth"] > theirs[s]["max_depth"]]

    delta = data["mean_progress"] - parent["mean_progress"]
    lines = [
        f"  seeds moved at all: {len(changed)}/{len(shared)}"
        f"   (forward {len(improved)}, backward {len(regressed)})",
        f"  seeds unchanged:    {len(still)}/{len(shared)}",
        f"  of the moved seeds, progression rose on {len(prog_up)} "
        f"and fell on {len(prog_down)}",
        f"  seeds reaching a deeper level: {len(deeper)}/{len(shared)}",
        f"  mean progression delta {delta:+.4f}",
    ]
    if not changed:
        lines.append("  nothing changed on any seed: this tree is the parent.")
    elif len(still) >= len(shared) - 2:
        lines.append(
            f"  {len(still)} of {len(shared)} seeds are bit-identical: the change "
            "barely fires, and the whole delta lives in the seeds that differ."
        )
    if changed:
        lines.append(f"  moved seeds: {changed}")
    if dropped:
        lines.append(
            f"  EXCLUDED as unstable under repeated scoring: {dropped}"
        )

    # Verdict. The primary requirement is REACH -- a mutation that touches one
    # or two seeds has not demonstrated anything. Direction is then judged on
    # the count of seeds moving forward, because N3a showed progression is too
    # coarse to arbitrate on its own: its SE of the mean is 0.0281, larger than
    # any single change this loop makes, so a small negative mean is not on its
    # own evidence of harm. `deeper` is reported for context, and is used only
    # to break a tie between equal forward counts, never to overrule a majority
    # that moved backwards.
    if not changed:
        verdict, why = "NOT-A-WIN", "no seed moved on any signal"
    elif len(changed) < MIN_SEEDS_MOVED:
        verdict, why = "NOT-A-WIN", (
            f"only {len(changed)} seed(s) moved, below the {MIN_SEEDS_MOVED} "
            "needed to show the change reaches more than a fluke"
        )
    elif len(regressed) >= len(improved):
        verdict, why = "NOT-A-WIN", (
            f"of the {len(changed)} seeds that moved, at least as many went "
            f"backwards ({len(regressed)}) as forwards ({len(improved)})"
        )
    elif delta <= 0 and not deeper:
        verdict, why = "NOT-A-WIN", (
            f"mean progression {delta:+.4f} and no seed reached a deeper level"
        )
    else:
        verdict = "WIN"
        why = (
            f"{len(changed)} seeds moved ({len(improved)} forward, "
            f"{len(regressed)} back), mean {delta:+.4f}, {len(deeper)} deeper"
        )

    return verdict, "\n".join([f"  {why}", *lines])


def load_stable(path: str | None) -> set[int] | None:
    """Seeds that survived repeated scoring of one tree. None when unknown."""
    if not path:
        return None
    data = json.load(open(path))
    stable = data.get("stable_seeds")
    if stable is None:
        return None
    return set(stable)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    stable_from = None
    if "--stable-from" in sys.argv:
        stable_from = load_stable(sys.argv[sys.argv.index("--stable-from") + 1])
    data = json.load(open(args[0]))
    expected = float(args[1]) if len(args) > 1 else 0.0

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
    if stable_from is None:
        print("  (no stable-seed list supplied: every seed counted)")
    else:
        print("  unstable seeds excluded via --stable-from")
    paired = paired_verdict(data, stable_from)
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
