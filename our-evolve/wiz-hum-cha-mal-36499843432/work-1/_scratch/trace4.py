"""Attribute every Agent.step to the innermost strategy that issued it."""
import os
import re
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
from autoascend import strategy as strat  # noqa: E402
from autoascend import agent as aa  # noqa: E402

CHARACTER = "wiz-hum-cha-mal"
STACK = []
HOLDER = {}
COUNTS = Counter()
PHASES = []  # (turn, label) transitions


def label(cfg):
    s = str(cfg)
    fns = re.findall(r"<function ([A-Za-z_0-9.]+)", s)
    if fns:
        return ".".join(f.split(".")[-1] for f in fns[:2])
    return s[:40]


def instrument():
    orig_run = strat.Strategy.run

    def run(self, return_condition=False):
        HOLDER["agent"] = self  # only used to keep a ref
        STACK.append(label(self.config))
        try:
            return orig_run(self, return_condition)
        finally:
            STACK.pop()

    strat.Strategy.run = run

    orig_step = aa.Agent.step

    def step(self, action, additional_action_iterator=None):
        lab = STACK[-1] if STACK else "<none>"
        COUNTS[lab] += 1
        PHASES.append((self._last_turn, lab))
        return orig_step(self, action, additional_action_iterator)

    aa.Agent.step = step


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 13
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
    total = sum(COUNTS.values()) or 1
    print(f"{'steps':>8} {'share':>6}  innermost strategy")
    for k, v in COUNTS.most_common(25):
        print(f"{v:8d} {v/total:6.1%}  {k}")
    if len(sys.argv) > 2:
        print("--- timeline (turn, label) ---")
        prev = None
        for turn, lab in PHASES:
            if lab != prev:
                print(f"  {turn:6d} {lab}")
                prev = lab
    env.close()


if __name__ == "__main__":
    main()
