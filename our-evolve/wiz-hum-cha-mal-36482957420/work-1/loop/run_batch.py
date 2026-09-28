"""Run several arena seeds in separate processes and print a per-seed table.

Usage: python loop/run_batch.py <tree_dir> [seed ...]
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run_one(tree: str, seed: int, max_turns: int) -> dict:
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "run_local.py"), tree, str(seed), str(max_turns)],
        capture_output=True, text=True, cwd=tree, timeout=7200,
    )
    line = [ln for ln in proc.stdout.splitlines() if ln.startswith("{")]
    if not line:
        return {"seed": seed, "status": "crash", "progress": 0.0, "turns": 0, "depth": 1,
                "cause": proc.stderr.strip().splitlines()[-1][:80] if proc.stderr else "?"}
    return json.loads(line[-1])


def main() -> None:
    tree = os.path.abspath(sys.argv[1])
    seeds = [int(s) for s in sys.argv[2:]] or list(range(15))
    max_turns = int(os.environ.get("MAX_TURNS", "60000"))
    workers = int(os.environ.get("WORKERS", "4"))
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_one, tree, s, max_turns): s for s in seeds}
        for fut in concurrent.futures.as_completed(futs):
            r = fut.result()
            out[r["seed"]] = r
            print(f"seed {r['seed']:>3}  {r['progress']:.4f}  turns={r['turns']:>6}  "
                  f"dl={r['depth']}  {str(r.get('cause'))[:28]}", flush=True)
    print()
    print("| seed | turns | deepest | progress | died of |")
    print("| --- | --- | --- | --- | --- |")
    for s in sorted(out):
        r = out[s]
        print(f"| {s} | {r['turns']} | {r['depth']} | {r['progress']:.4f} | {r.get('cause')} |")
    mean = statistics.mean(out[s]["progress"] for s in out)
    print(f"\nmean {mean:.4f} over {len(out)} seeds")


if __name__ == "__main__":
    main()
