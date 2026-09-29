"""Count which NetHack actions the bot issues, per run."""
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
ACT = Counter()
STATE = {"killed": 0, "faint": 0, "searches": 0}


def instrument():
    from autoascend import agent as aa

    orig_step = aa.Agent.step

    def step(self, action, additional_action_iterator=None):
        ACT[aa.A.Command(action).name] += 1
        return orig_step(self, action, additional_action_iterator)

    aa.Agent.step = step

    orig_search = aa.Agent.search

    def search(self):
        STATE["searches"] += 1
        return orig_search(self)

    aa.Agent.search = search

    orig_melee = aa.Agent.melee_attack

    def melee_attack(self, y, x):
        STATE["killed"] += 0
        return orig_melee(self, y, x)

    aa.Agent.melee_attack = melee_attack


def run(seed):
    import random

    import numpy as np

    from bot import make_agent

    ACT.clear(); STATE.update(killed=0, faint=0, searches=0)
    spec = trajectory_spec("public", "local", seed)
    env = make_environment(1_000_000, 10_000, CHARACTER)
    random.seed(spec.bot_seed)
    np.random.seed(spec.bot_seed % (1 << 32))
    bot = make_agent()
    obs = env.reset(spec)
    bot.reset(obs)

    import nle.nethack as nh
    ACTIONS = tuple(nh.ACTIONS)

    def loop():
        nonlocal obs
        while True:
            action = bot.act(obs)
            try:
                ACT[ACTIONS[action].name] += 1
            except Exception:
                ACT[str(action)] += 1
            obs, _r, term, trunc = env.step(action)
            if term or trunc:
                break

    t = threading.Thread(target=loop)
    t.start()
    t.join()
    m = env.metrics()
    total = sum(ACT.values()) or 1
    env.close()
    return {
        "seed": seed, "prog": round(m.progress, 5), "turns": m.turns, "cause": m.cause_of_death,
        "steps": total,
        "top": [(k, v, f"{v/total:.1%}") for k, v in ACT.most_common(14)],
    }


if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [0, 12, 14]
    for s in seeds:
        r = run(s)
        print(f"--- seed {r['seed']} prog {r['prog']} turns {r['turns']} cause {r['cause']} steps {r['steps']}",
              flush=True)
        for k, v, p in r["top"]:
            print(f"      {k:<18} {v:>7}  {p}", flush=True)
