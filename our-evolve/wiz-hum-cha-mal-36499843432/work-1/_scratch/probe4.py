"""Count food intake vs corpses encountered, and hunger-state history."""
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
HUNGER_NAMES = {0: "SATIATED", 1: "NOT_HUNGRY", 2: "HUNGRY", 3: "WEAK",
                4: "FAINTING", 5: "FAINTED", 6: "FAINTED_FASTER"}
COUNTS = Counter()
TRANS = []
EATS = []
NUT = []


def instrument():
    from autoascend.item import inventory as inv_mod

    orig_eat = inv_mod.Inventory.eat

    def eat(self, item, *a, **kw):
        r = orig_eat(self, item, *a, **kw)
        nut = 0
        try:
            nut = int(item.nutrition)
        except Exception:
            nut = 0
        EATS.append((str(item.object.name), nut))
        COUNTS["eat_calls"] += 1
        return r

    inv_mod.Inventory.eat = eat

    orig_cede = None


def run(seed):
    import random

    import numpy as np

    from bot import make_agent

    instrument()
    EATS.clear(); TRANS.clear()
    spec = trajectory_spec("public", "local", seed)
    env = make_environment(1_000_000, 10_000, CHARACTER)
    random.seed(spec.bot_seed)
    np.random.seed(spec.bot_seed % (1 << 32))
    bot = make_agent()
    obs = env.reset(spec)
    bot.reset(obs)
    st = {"prev": -1, "killed": 0, "corpse_tiles": 0, "n": 0, "min_hp_frac": 1.0}

    def loop():
        nonlocal obs
        a = bot._driver._agent
        while True:
            bl = obs["blstats"]
            h = int(bl[21])
            if h != st["prev"]:
                TRANS.append((st["n"], HUNGER_NAMES.get(h, h), int(bl[18])))
                st["prev"] = h
            hp, hpm = int(bl[10]), int(bl[11])
            if hpm > 0:
                st["min_hp_frac"] = min(st["min_hp_frac"], hp / hpm)
            try:
                lv = a.current_level()
                st["corpse_tiles"] = sum(1 for k, v in lv.corpses_to_eat.items() if v)
            except Exception:
                pass
            action = bot.act(obs)
            obs, _r, term, trunc = env.step(action)
            st["n"] += 1
            if term or trunc:
                break

    t = threading.Thread(target=loop)
    t.start()
    t.join()
    m = env.metrics()
    bl = obs["blstats"]
    nut = sum(n for _, n in EATS if n > 0)
    env.close()
    return {
        "seed": seed, "prog": round(m.progress, 5), "turns": m.turns, "cause": m.cause_of_death,
        "xl": int(bl[18]), "hunger_end": HUNGER_NAMES.get(int(bl[21])),
        "eat_calls": len(EATS), "nutrition": nut,
        "avg_nut": round(nut / max(1, len(EATS)), 1),
        "min_hp_frac": round(st["min_hp_frac"], 2),
        "transitions": TRANS,
        "eats": EATS[:40],
        "hunger_hist": {k: TRANS.count if 0 else sum(1 for t in TRANS if t[1] == k) for k in
                        ["HUNGRY", "WEAK", "FAINTING", "FAINTED", "FAINTED_FASTER"]},
    }


if __name__ == "__main__":
    for s in ([int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [0]):
        r = run(s)
        print(f"seed {r['seed']} prog {r['prog']} turns {r['turns']} cause {r['cause']} "
              f"xl {r['xl']} hunger_end {r['hunger_end']} eat_calls {r['eat_calls']} "
              f"nutrition {r['nutrition']} avg {r['avg_nut']} min_hp_frac {r['min_hp_frac']}", flush=True)
        print("  hunger transitions:", r["transitions"], flush=True)
        print("  hunger_hist:", r["hunger_hist"], flush=True)
        print("  eats:", r["eats"], flush=True)
