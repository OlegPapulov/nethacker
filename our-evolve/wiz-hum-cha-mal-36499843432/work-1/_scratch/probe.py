"""Run the 15 public seeds and dump end-of-run state + message keywords."""
import os
import sys
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

CHARACTER = "wiz-hum-cha-mal"
KEYS = ["faint", "Goodbye level", "Thou art", "hear again", "weak", "hungry",
        "food", "prayer", "spell", "energy", "cold", "hallucinat", "poison"]


def run(seed):
    import random

    import numpy as np

    from bot import make_agent

    spec = trajectory_spec("public", "local", seed)
    env = make_environment(1_000_000, 10_000, CHARACTER)
    random.seed(spec.bot_seed)
    np.random.seed(spec.bot_seed % (1 << 32))
    agent = make_agent()
    obs = env.reset(spec)
    agent.reset(obs)
    info = {"bl": None, "n": 0, "msgs": [], "xpmax": 1, "depthmax": 1}
    msgset = set()

    def loop():
        nonlocal obs
        while True:
            bl = obs["blstats"]
            if bl[18] > info["xpmax"]:
                info["xpmax"] = int(bl[18])
            if bl[24] > info["depthmax"]:
                info["depthmax"] = int(bl[24])
            info["bl"] = bl.copy()
            for m in obs.get("message", []):
                m = str(m).strip()
                if m:
                    msgset.add(m)
            action = agent.act(obs)
            obs, _r, term, trunc = env.step(action)
            info["n"] += 1
            if term or trunc:
                break

    t = threading.Thread(target=loop)
    t.start()
    t.join()
    m = env.metrics()
    bl = info["bl"]
    hits = {k: sum(1 for s in msgset if k.lower() in s.lower()) for k in KEYS}
    hits = {k: v for k, v in hits.items() if v}
    env.close()
    return {
        "seed": seed, "prog": round(m.progress, 5), "turns": m.turns,
        "cause": m.cause_of_death, "hp": int(bl[10]), "hpmax": int(bl[11]),
        "xl": int(bl[18]), "xpmax": info["xpmax"], "depthmax": info["depthmax"],
        "depth": int(bl[24]), "hunger": int(bl[21]), "energy": int(bl[14]), "con": int(bl[5]),
        "ac": int(bl[16]), "msgs": hits,
    }


if __name__ == "__main__":
    seeds = range(15)
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1].split(",")]
    for s in seeds:
        print(run(s), flush=True)
