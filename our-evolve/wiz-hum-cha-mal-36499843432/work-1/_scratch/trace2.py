"""Trace which strategies run and for how long."""
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
from autoascend import agent as aa  # noqa: E402

CHARACTER = "wiz-hum-cha-mal"

EVENTS = []
AGENT_HOLDER = {}


def _name(cfg):
    s = str(cfg)
    return s[:70]


def instrument():
    orig_preempt = aa.Agent.preempt

    def preempt(self, strategies, func, first_func=None, continue_after_preemption=True):
        AGENT_HOLDER["agent"] = self
        t0 = self.step_count
        tr0 = self._last_turn
        names = [_name(s.config) for s in strategies]
        EVENTS.append((self._last_turn, "preempt", names, func))
        return orig_preempt(self, strategies, func, first_func, continue_after_preemption)

    aa.Agent.preempt = preempt


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    every = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    instrument()
    from bot import make_agent

    spec = trajectory_spec("public", "local", seed)
    env = make_environment(1_000_000, 10_000, CHARACTER)
    obs = env.reset(spec)
    agent = make_agent()
    agent.reset(obs)
    state = {"steps": 0, "obs": obs}

    def loop():
        nonlocal obs
        obs = state["obs"]
        while state["steps"] < 1_000_000:
            action = agent.act(obs)
            obs, _r, term, trunc = env.step(action)
            state["steps"] += 1
            if term or trunc:
                break

    t = threading.Thread(target=loop)
    t.start()
    t.join()
    m = env.metrics()
    print("progress", m.progress, "turns", m.turns, "depth", m.max_depth, "cause", m.cause_of_death)
    ag = AGENT_HOLDER.get("agent")
    if ag is not None:
        print("strategy events:", len(EVENTS))
        prev = 0
        from collections import Counter
        c = Counter()
        for turn, kind, names, func in EVENTS:
            if every > 1 and (turn // every) != (prev // every):
                prev = turn
                continue
            c[str(names)[:120]] += 1
        for k, v in c.most_common(30):
            print(f"  {v:5d}  {k}")
    env.close()


if __name__ == "__main__":
    main()
