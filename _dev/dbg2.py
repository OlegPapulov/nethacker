"""Instrumented local run: count where the agent spends its turns."""
import argparse
import importlib
import json
import os
import sys
import time
import warnings
from collections import Counter

os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")

from nethackers.arena.environment import make_environment
from nethackers.arena.progress import NetHackProgress
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh

p = argparse.ArgumentParser()
p.add_argument("--seed", type=int, default=0)
p.add_argument("--character", default="wiz-hum-cha-mal")
p.add_argument("--trace", type=int, default=0)
p.add_argument("--solution", default="/workspace")
a = p.parse_args()

sys.path.insert(0, a.solution)
bot_mod = importlib.import_module("bot")

spec = trajectory_spec("public", "local", a.seed)
env = make_environment(1_000_000, 10_000, a.character)
bot = bot_mod.make_agent()
obs = env.reset(spec)
bot.reset(obs)
drv = bot._driver
agent = drv._agent
import time as _t
for _ in range(200):
    if agent is not None and hasattr(agent, 'blstats'):
        break
    _t.sleep(0.05)

counters = Counter()
orig = {}


def wrap(name, obj, label=None):
    label = label or name
    f = getattr(obj, name)

    def g(*args, **kwargs):
        counters[label] += 1
        return f(*args, **kwargs)
    setattr(obj, name, g)


for n in ['move', 'search', 'melee_attack', 'direction', 'fire', 'zap', 'go_to',
          'untrap', 'pickup' if False else 'open_door', 'kick', 'pray', 'cast']:
    if hasattr(agent, n):
        wrap(n, agent, 'agent.' + n)
for n in ['explore1', 'go_to_strategy', 'explore_stairs', 'patrol', 'go_to_level_strategy']:
    if hasattr(agent.exploration, n):
        wrap(n, agent.exploration, 'expl.' + n)
for n in ['inventory', 'items', 'gold']:
    pass
# inventory ops
inv = agent.inventory
for n in ['gather_items', 'eat', 'quaff', 'wield', 'pickup', 'arrange_items', 'drop']:
    if hasattr(inv, n):
        wrap(n, inv, 'inv.' + n)

started = time.time()
steps = 0
prog = NetHackProgress()
snap = Counter()
last_log = 0
while True:
    action = bot.act(obs)
    obs, _r, term, trunc = env.step(action)
    steps += 1
    prog.update(obs)
    t = int(obs["blstats"][nh.NLE_BL_TIME])
    if a.trace and t - last_log >= a.trace:
        last_log = t
        delta = {k: v - snap[k] for k, v in counters.items() if v - snap[k] > 0}
        snap = Counter(counters)
        bs = obs["blstats"]
        print(f"t={t} d={bs[nh.NLE_BL_DEPTH]} xp={bs[nh.NLE_BL_XP]} hp={bs[nh.NLE_BL_HP]} "
              f"hung={bs[nh.NLE_BL_HUNGER]} prog={prog.progression:.3f} {delta}", flush=True)
    if term or trunc:
        break
m = env.metrics()
print(json.dumps(dict(seed=a.seed, progress=m.progress, turns=m.turns, depth=m.max_depth,
                      milestone=m.milestone, cause=m.cause_of_death, wall=round(time.time() - started, 1))))
print("totals:", json.dumps(dict(counters.most_common())))
drv_env = env.metrics()
try:
    st = {k: v for k, v in agent.stats_logger.get_stats_dict().items() if v}
    print("stats:", {k: (int(v) if hasattr(v, '__index__') or isinstance(v, int) else round(float(v), 2))
                     for k, v in st.items()})
except Exception as e:
    print("stats err", e)
if drv.thread_error:
    print("thread_error:", drv.thread_error[-1500:])