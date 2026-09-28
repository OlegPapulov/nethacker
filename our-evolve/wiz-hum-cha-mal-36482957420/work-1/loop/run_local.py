"""Local replica of the arena episode loop, for measuring per-seed results.

Usage: python loop/run_local.py <tree_dir> <seed> [max_turns]
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import time


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tree")
    p.add_argument("seed", type=int)
    p.add_argument("max_turns", type=int, default=60000)
    p.add_argument("--bot-seed", type=int, default=0)
    args = p.parse_args()

    tree = os.path.abspath(args.tree)
    sys.path.insert(0, tree)

    from nethackers.arena.environment import make_environment
    from nethackers.arena.seeds import trajectory_spec
    import nethackers.contracts.models as models

    spec = trajectory_spec("public", "local", args.seed)

    env = make_environment(models.DEFAULT_MAX_STEPS, models.DEFAULT_NO_PROGRESS_TIMEOUT,
                           character="wiz-hum-cha-mal")
    agent = None
    try:
        obs = env.reset(spec)
        bot_mod = importlib.import_module("bot")
        agent = bot_mod.make_agent()
        # arena seeds the bot's RNGs with spec.bot_seed
        import random as _random
        import numpy as _np
        _random.seed(args.bot_seed)
        _np.random.seed(args.bot_seed % (1 << 32))
        agent.reset(obs)

        t0 = time.time()
        turns = 0
        best = 0.0
        depth = 1
        steps = 0
        status = "running"
        while True:
            action = agent.act(obs)
            obs, reward, terminated, truncated = env.step(action)
            steps += 1
            m = env.metrics()
            best = max(best, m.progress)
            depth = max(depth, m.max_depth)
            turns = max(turns, m.turns)
            if m.turns > args.max_turns:
                status = "turn_cap"
                break
            if terminated or truncated:
                status = "ended"
                break
        m = env.metrics()
        print(json.dumps({
            "seed": args.seed, "status": status, "progress": round(max(best, m.progress), 4),
            "turns": turns, "depth": depth, "steps": steps,
            "milestone": m.milestone, "cause": m.cause_of_death,
            "seconds": round(time.time() - t0, 1),
        }))
    finally:
        try:
            if agent is not None:
                agent.close()
        except Exception:
            pass
        env.close()


if __name__ == "__main__":
    main()
