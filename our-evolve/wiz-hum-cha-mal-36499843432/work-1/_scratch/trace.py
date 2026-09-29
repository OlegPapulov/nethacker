"""Trace one episode: state timeline + last messages before death."""
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

import numpy as np  # noqa: E402
from nethackers.arena.environment import make_environment  # noqa: E402
from nethackers.arena.seeds import trajectory_spec  # noqa: E402

CHARACTER = "wiz-hum-cha-mal"
BL_TIME, BL_DLEVEL, BL_HP, BL_HPMAX = 20, 24, 10, 11
BL_XP, BL_XPPOINTS, BL_ENERGY, BL_HUNGER, BL_SCORE, BL_GOLD = 18, 19, 14, 21, 9, 13


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    from bot import make_agent
    import autoascend.agent as aa

    spec = trajectory_spec("public", "local", seed)
    env = make_environment(1_000_000, 10_000, CHARACTER)
    obs = env.reset(spec)
    agent = make_agent()
    agent.reset(obs)
    # the driver holds the Agent instance; grab it from the thread via the env shim
    drv = agent._driver
    state = {"steps": 0, "obs": obs, "hist": [], "msgs": [], "log": []}

    orig_step = aa.Agent.step

    def traced_step(self, action, additional_action_iterator=None):
        return orig_step(self, action, additional_action_iterator)

    def loop():
        nonlocal obs
        obs = state["obs"]
        while state["steps"] < 1_000_000:
            action = agent.act(obs)
            prev = obs
            obs, _r, term, trunc = env.step(action)
            state["steps"] += 1
            bl = obs["blstats"]
            m = bytes(obs["message"]).decode().replace("\0", " ").replace("\n", " ").strip()
            if m:
                state["msgs"].append((int(bl[BL_TIME]), m))
            if state["steps"] % 200 == 0:
                state["hist"].append((state["steps"], int(bl[BL_TIME]), int(bl[BL_DLEVEL]),
                                      int(bl[BL_HP]), int(bl[BL_HPMAX]), int(bl[BL_XP]),
                                      int(bl[BL_ENERGY]), int(bl[BL_HUNGER])))
            if term or trunc:
                break

    t = threading.Thread(target=loop)
    t.start()
    t.join()
    m = env.metrics()
    print("progress", m.progress, "turns", m.turns, "depth", m.max_depth, "cause", m.cause_of_death)
    print("steps", state["steps"])
    print("  step turn dlvl  hp/hpmax xl energy hunger")
    for row in state["hist"]:
        print("  ", row)
    print("--- last 40 messages ---")
    for tt, msg in state["msgs"][-int(os.environ.get("NMSG","40")):]:
        print(f"  [{tt}] {msg}")
    env.close()


if __name__ == "__main__":
    main()
