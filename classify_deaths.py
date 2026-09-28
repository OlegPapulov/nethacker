"""E2: group the ten dlvl-1 deaths into distinct bugs, from tracing runs.

E1 found AutoAscend scores 0.0624 on wiz-hum-cha-mal with **10 of 15 seeds never
leaving dlvl 1**. Before spending an agent on "improve early combat" it is worth
knowing whether those ten deaths are even the same bug -- because two of them
(grid bug at 3,052 turns, starvation at 5,206) are not combat deaths and happen
four times earlier than the combat ones at 12k-22k.

This reads the JSON traces written by ``tracing_bot.py`` and sorts every seed into
one of five buckets, by what the bot was actually doing:

``AMBUSHED``   adjacent to a monster late, not attacking, HP falling
``OUTFOUGHT``  adjacent and attacking, HP falling -- it fought and lost
``STARVED``    never in contact, dying of hunger or a non-combat cause
``NO-COMBAT``  never in contact, but died in combat to something it never met
``CLEAN``      survived, or died at high HP with no sustained contact

The point is not the bucket names. It is that a fix aimed at one bucket can only
ever move that bucket's seeds, so the buckets decide what the next experiment
should attempt.

Usage: classify_deaths.py <trace-dir> <diagnosis.json> [out.json]
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

#: A seed counts as "in contact" if it spent at least this fraction of its
#: turns next to a monster. Low, because a single corridor squeeze is contact.
CONTACT_FRACTION = 0.01

#: HP below this fraction counts as "beaten".
LOW_HP = 0.5


def load_traces(trace_dir: Path) -> dict[int, dict]:
    traces: dict[int, dict] = {}
    for path in sorted(trace_dir.glob("trace-*.json")):
        try:
            seed = int(path.stem.split("-")[-1])
        except ValueError:
            continue
        try:
            traces[seed] = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
    return traces


def classify(trace: dict, death: str | None, depth: int) -> tuple[str, str]:
    total = max(1, int(trace.get("total_turns") or 1))
    adjacent = int(trace.get("adjacent_turns") or 0)
    attacking = int(trace.get("attacking_turns") or 0)
    tail = trace.get("tail") or []

    hp_frac = None
    hunger_end = None
    if tail:
        last = tail[-1]
        if last.get("maxhp"):
            hp_frac = last["hp"] / last["maxhp"]
        hunger_end = last.get("hunger")

    contact = adjacent / total >= CONTACT_FRACTION
    reason_death = (death or "unknown").lower()
    non_combat = any(
        w in reason_death
        for w in ("starvation", "grid bug", "choked", "drowning", "drowned")
    )

    if depth <= 1 and not contact and non_combat:
        return (
            "STARVED",
            f"never in contact with a monster over {total} turns, died of "
            f"{death!r} at dlvl {depth}; hunger {hunger_end} at the end",
        )
    if not contact:
        return (
            "NO-COMBAT",
            f"never within one square of a monster over {total} turns; died of "
            f"{death!r} at dlvl {depth}",
        )
    if attacking == 0:
        return (
            "AMBUSHED",
            f"contact on {adjacent} turns and 0 non-movement actions, so it "
            f"never fought; died of {death!r} at dlvl {depth}",
        )
    if hp_frac is not None and hp_frac < LOW_HP:
        return (
            "OUTFOUGHT",
            f"contact on {adjacent} turns with {attacking} non-movement actions "
            f"and HP down to {hp_frac:.0%}; fought and lost to {death!r}",
        )
    return (
        "DIED-HIGH",
        f"contact on {adjacent} turns, {attacking} non-movement actions, HP "
        f"{'unknown' if hp_frac is None else format(hp_frac, '.0%')}; "
        f"died of {death!r} at dlvl {depth}",
    )


def main() -> None:
    trace_dir = Path(sys.argv[1])
    diagnosis = json.loads(Path(sys.argv[2]).read_text())
    out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    traces = load_traces(trace_dir)
    results = {int(r["seed"]): r for r in diagnosis["results"]}

    rows = []
    for seed in sorted(results):
        result = results[seed]
        trace = traces.get(seed)
        if trace is None:
            verdict, reason = "NO-TRACE", "no trace captured for this seed"
        else:
            verdict, reason = classify(
                trace, result.get("death"), int(result.get("depth") or 0)
            )
        rows.append(
            {
                "seed": seed,
                "verdict": verdict,
                "reason": reason,
                "turns": result.get("turns"),
                "depth": result.get("depth"),
                "progress": result.get("progress"),
                "death": result.get("death"),
                "adjacent_turns": (trace or {}).get("adjacent_turns"),
                "attacking_turns": (trace or {}).get("attacking_turns"),
            }
        )

    counts: Counter[str] = Counter(r["verdict"] for r in rows)
    by_verdict: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        by_verdict[row["verdict"]].append(row["seed"])

    dlvl1 = [r for r in rows if (r["depth"] or 0) <= 1]
    dlvl1_counts: Counter[str] = Counter(r["verdict"] for r in dlvl1)

    print(f"traces found: {len(traces)} of {len(results)} seeds")
    print()
    print("=== all seeds ===")
    for verdict, seeds in sorted(by_verdict.items(), key=lambda kv: -len(kv[1])):
        print(f"  {verdict:10} n={len(seeds):2}  seeds {seeds}")
    print()
    print(f"=== the {len(dlvl1)} seeds that never left dlvl 1 ===")
    for verdict, count in dlvl1_counts.most_common():
        print(f"  {verdict:10} n={count}")
    print()
    for row in rows:
        print(f"  {row['seed']:>2} {row['verdict']:10} {row['reason'][:78]}")

    payload = {
        "verdicts": dict(counts),
        "dlvl1_verdicts": dict(dlvl1_counts),
        "by_verdict": {k: v for k, v in by_verdict.items()},
        "rows": rows,
    }
    if out_path:
        out_path.write_text(json.dumps(payload, indent=2))
    print()
    print("DLVL1 " + json.dumps(dict(dlvl1_counts)))


if __name__ == "__main__":
    main()
