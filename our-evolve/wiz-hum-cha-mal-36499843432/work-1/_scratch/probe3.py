"""Track armor acquisition: what the wizard ever sees, wears, and max AC."""
import os
import sys
import warnings
from collections import Counter

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
LOG = []


def instrument():
    from autoascend.item import inventory as inv_mod

    orig_wear = inv_mod.Inventory.wear

    def wear(self, item, smart=True):
        r = orig_wear(self, item, smart)
        LOG.append(("wear", str(item.object.name), str(item.status), r))
        return r

    inv_mod.Inventory.wear = wear

    orig_takeoff = inv_mod.Inventory.takeoff

    def takeoff(self, item):
        LOG.append(("takeoff", str(item.object.name), str(item.status), ""))
        return orig_takeoff(self, item)

    inv_mod.Inventory.takeoff = takeoff

    orig_best = inv_mod.Inventory.get_best_armorset

    def best(self, items=None, **kw):
        return orig_best(self, items, **kw)

    inv_mod.Inventory.get_best_armorset = best


def run(seed):
    import random

    import numpy as np

    from bot import make_agent

    instrument()
    spec = trajectory_spec("public", "local", seed)
    env = make_environment(1_000_000, 10_000, CHARACTER)
    random.seed(spec.bot_seed)
    np.random.seed(spec.bot_seed % (1 << 32))
    bot = make_agent()
    obs = env.reset(spec)
    bot.reset(obs)
    stats = {"maxac": 99, "minac": -99, "n": 0}
    seen_armor = Counter()

    def loop():
        nonlocal obs
        while True:
            a = bot._driver._agent
            try:
                ac = int(obs["blstats"][5])
                if ac < stats["minac"]:
                    stats["minac"] = ac
            except Exception:
                pass
            try:
                for it in a.inventory.items:
                    if it.is_armor() and it.is_unambiguous():
                        seen_armor[(it.object.name, str(it.status), it.equipped)] += 1
            except Exception:
                pass
            action = bot.act(obs)
            obs, _r, term, trunc = env.step(action)
            stats["n"] += 1
            if term or trunc:
                break

    t = threading.Thread(target=loop)
    t.start()
    t.join()
    m = env.metrics()
    env.close()
    return {
        "seed": seed, "prog": round(m.progress, 5), "xl_turns": m.turns,
        "cause": m.cause_of_death, "minac": stats["minac"],
        "wear_log": [x for x in LOG if x[0] == "wear"],
        "armor_in_inv_at_end": sorted(seen_armor.items(), key=lambda kv: -kv[1])[:12],
    }


if __name__ == "__main__":
    for s in ([int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [3]):
        r = run(s)
        print("seed", r["seed"], "prog", r["prog"], "turns", r["xl_turns"], "cause", r["cause"],
              "minac", r["minac"], flush=True)
        print("  WEAR LOG:", r["wear_log"], flush=True)
        print("  ARMOR SEEN:", r["armor_in_inv_at_end"], flush=True)
