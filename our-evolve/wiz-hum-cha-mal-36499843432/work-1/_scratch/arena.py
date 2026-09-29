"""Faithful local replica of the nethackers arena runner (public seeds 0..14).

Uses /opt/kit/nethackers arena code verbatim so candidate/parent comparisons are
paired with the real evaluator: same NLE task, same options, same seeds, same
progression metric.
"""
import argparse
import json
import os
import sys
import time
import warnings

sys.setrecursionlimit(100000)
sys.path.insert(0, "/opt/kit")
sys.path.insert(0, "/workspace")

import threading  # noqa: E402

threading.stack_size(1024 * 1024 * 1024)

os.environ.setdefault("XDG_CACHE_HOME", "/workspace/_scratch/cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/workspace/_scratch/cache/numba")
warnings.filterwarnings("ignore", category=RuntimeWarning)

from nethackers.arena.environment import make_environment  # noqa: E402
from nethackers.arena.seeds import trajectory_spec  # noqa: E402
from nethackers.contracts.models import Objective  # noqa: E402

CHARACTER = "wiz-hum-cha-mal"
MAX_STEPS = 1_000_000
NO_PROGRESS_TIMEOUT = 10_000
SECRET = "public"
EVAL_ID = "local"


def run_one(seed, max_steps=MAX_STEPS, tag=""):
    import random

    import numpy as np

    from bot import make_agent

    spec = trajectory_spec(SECRET, EVAL_ID, seed)
    objective = Objective(CHARACTER, max_steps, NO_PROGRESS_TIMEOUT, 120.0, "runtime")

    env = None
    t0 = time.monotonic()
    steps = 0
    err = None
    try:
        env = make_environment(objective.max_steps, objective.no_progress_timeout,
                               objective.character)
        # the arena's sandbox seeds the *bot* process; mirror it for the in-process bot
        random.seed(spec.bot_seed)
        np.random.seed(spec.bot_seed % (1 << 32))

        agent = make_agent()
        obs = env.reset(spec)
        agent.reset(obs)

        state = {"stop": False}

        def loop():
            nonlocal obs, steps
            while not state["stop"] and steps < max_steps:
                action = agent.act(obs)
                obs, _r, terminated, truncated = env.step(action)
                steps += 1
                if terminated or truncated:
                    break

        t = threading.Thread(target=loop)
        t.start()
        t.join()
        m = env.metrics()
        return {
            "seed": seed, "tag": tag, "status": "completed",
            "progress": m.progress, "turns": m.turns, "max_depth": m.max_depth,
            "ascended": m.ascended, "end_status": m.end_status,
            "milestone": m.milestone, "cause": m.cause_of_death,
            "steps": steps, "wall": round(time.monotonic() - t0, 1),
            "err": err,
        }
    except BaseException:
        import traceback
        if env is not None:
            m = env.metrics()
        return {
            "seed": seed, "tag": tag, "status": "error", "progress": 0.0,
            "turns": getattr(m, "turns", 0) if env is not None else 0,
            "max_depth": getattr(m, "max_depth", 1) if env is not None else 1,
            "ascended": False, "end_status": None, "milestone": None, "cause": None,
            "steps": steps, "wall": round(time.monotonic() - t0, 1),
            "err": traceback.format_exc(limit=20)[-4000:],
        }
    finally:
        if env is not None:
            try:
                env.close()
            except Exception:
                pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="0-14")
    ap.add_argument("--max-steps", type=int, default=MAX_STEPS)
    ap.add_argument("--out", default="")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    if "-" in a.seeds:
        lo, hi = a.seeds.split("-")
        seeds = list(range(int(lo), int(hi) + 1))
    else:
        seeds = [int(s) for s in a.seeds.split(",")]
    rows = []
    for s in seeds:
        r = run_one(s, a.max_steps, a.tag)
        rows.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != "err"}), flush=True)
        if r.get("err"):
            print("   ERR:", r["err"][-1500:], flush=True)
    print("---- summary ----")
    print("mean_progress", round(sum(r["progress"] for r in rows) / len(rows), 5),
          " mean_depth", round(sum(r["max_depth"] for r in rows) / len(rows), 2),
          " mean_turns", round(sum(r["turns"] for r in rows) / len(rows), 1))
    if a.out:
        with open(a.out, "w") as f:
            json.dump(rows, f, indent=1)


if __name__ == "__main__":
    main()
