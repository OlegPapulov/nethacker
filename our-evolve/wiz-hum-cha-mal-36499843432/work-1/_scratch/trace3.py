"""Trace strategy stack: which strategy holds control for how many turns."""
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
from autoascend import strategy as strat  # noqa: E402
from autoascend import agent as aa  # noqa: E402

CHARACTER = "wiz-hum-cha-mal"
STACK = []
HOLDER = {}


def label(cfg):
    s = str(cfg)
    # compact: extract the most informative function name
    import re
    fns = re.findall(r"<function ([A-Za-z_0-9.]+)", s)
    extra = re.findall(r"'(until|repeat|preempt|condition|every)': ([^,}]+)", s)
    if fns:
        return ".".join(f.split(".")[-1] for f in fns[:3])
    return s[:50]


def instrument():
    orig_run = strat.Strategy.run

    def run(self, return_condition=False):
        agent = HOLDER.get("agent")
        turn = agent._last_turn if agent else -1
        STACK.append([label(self.config), turn, 0])
        try:
            return orig_run(self, return_condition)
        finally:
            entry = STACK.pop()
            if agent is not None:
                entry[2] = agent._last_turn - entry[1]
                OWN.setdefault(entry[0], [0, 0])
                OWN[entry[0]][0] += max(0, entry[2])
                OWN[entry[0]][1] += 1
            for e in STACK:
                e[2] = max(e[2], entry[2])

    strat.Strategy.run = run

    orig_preempt = aa.Agent.preempt

    def preempt(self, strategies, func, first_func=None, continue_after_preemption=True):
        HOLDER["agent"] = self
        return orig_preempt(self, strategies, func, first_func, continue_after_preemption)

    aa.Agent.preempt = preempt


OWN = {}


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
    total = m.turns or 1
    print(f"{'turns':>8} {'share':>6} {'n':>6}  strategy")
    for k, (tt, n) in sorted(OWN.items(), key=lambda kv: -kv[1][0])[:28]:
        print(f"{tt:8d} {tt/total:6.1%} {n:6d}  {k}")
    env.close()


if __name__ == "__main__":
    main()
