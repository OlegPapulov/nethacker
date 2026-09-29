"""Dump the wizard's final equipment / inventory to see why AC stays ~17."""
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
    box = {}
    seen_armor = set()
    seen_potions = set()

    def loop():
        nonlocal obs
        while True:
            try:
                inv = agent._driver._agent.inventory
                for it in inv.worn_items:
                    try:
                        seen_armor.add((str(it.object), str(it.status), it.get_ac()))
                    except Exception:
                        pass
                for it in inv.items:
                    try:
                        if it.category == 0 or "potion" in str(it.object):
                            seen_potions.add(str(it.object))
                    except Exception:
                        pass
            except Exception:
                pass
            action = agent.act(obs)
            obs, _r, term, trunc = env.step(action)
            if term or trunc:
                break

    t = threading.Thread(target=loop)
    t.start()
    t.join()
    m = env.metrics()
    inv = agent._driver._agent.inventory
    worn = []
    try:
        for it in inv.worn_items:
            worn.append((str(it.object), str(it.status), it.get_ac()))
    except Exception as e:
        worn = [("err", str(e), 0)]
    carried = []
    try:
        for it in inv.items:
            carried.append(str(it.object) + ("(worn)" if it.equipped else ""))
    except Exception:
        pass
    bl = obs["blstats"]
    env.close()
    return {
        "seed": seed, "prog": round(m.progress, 5), "xl": int(bl[18]), "ac": int(bl[5]),
        "hpmax": int(bl[4]), "turns": m.turns, "cause": m.cause_of_death,
        "worn_final": worn, "worn_seen": sorted(seen_armor),
        "carried": carried,
    }


if __name__ == "__main__":
    for s in ([int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [3, 10, 13]):
        r = run(s)
        print(r, flush=True)
