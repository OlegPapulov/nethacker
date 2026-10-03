"""Trace eating/hunger decisions for one seed."""
import argparse
import importlib
import json
import os
import sys
import warnings

os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")

from nethackers.arena.environment import make_environment
from nethackers.arena.progress import NetHackProgress
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh

p = argparse.ArgumentParser()
p.add_argument("--seed", type=int, default=4)
p.add_argument("--character", default="wiz-hum-cha-mal")
p.add_argument("--solution", default="/workspace")
p.add_argument("--every", type=int, default=250)
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

inv = agent.inventory
orig_eat = inv.eat


def eat(item, *args, **kwargs):
    try:
        name = item.objs[0].name
        mname = None
        try:
            mname = item.monster_id
        except Exception:
            pass
    except Exception:
        name, mname = '?', '?'
    r = orig_eat(item, *args, **kwargs)
    print(f"  t={agent.blstats.time} EAT {name} (mon={mname}) -> msg={agent.message[:70]!r} "
          f"hunger={agent.blstats.hunger_state} hp={agent.blstats.hitpoints}", flush=True)
    return r


inv.eat = eat

orig_quaff = inv.quaff


def quaff(item, *args, **kwargs):
    r = orig_quaff(item, *args, **kwargs)
    try:
        name = item.objs[0].name
    except Exception:
        name = '?'
    print(f"  t={agent.blstats.time} QUAFF {name} -> msg={agent.message[:70]!r} "
          f"hp={agent.blstats.hitpoints}", flush=True)
    return r


inv.quaff = quaff

last_hung = -1
last_log = 0
prog = NetHackProgress()
while True:
    action = bot.act(obs)
    obs, _r, term, trunc = env.step(action)
    prog.update(obs)
    t = int(obs["blstats"][nh.NLE_BL_TIME])
    hung = int(obs["blstats"][nh.NLE_BL_HUNGER])
    if hung != last_hung:
        print(f"t={t} HUNGER {last_hung} -> {hung} d={obs['blstats'][nh.NLE_BL_DEPTH]} "
              f"xp={obs['blstats'][nh.NLE_BL_XP]} hp={obs['blstats'][nh.NLE_BL_HP]}", flush=True)
        last_hung = hung
    if t - last_log >= a.every:
        last_log = t
        from autoascend.item import flatten_items
        foods = []
        for it in flatten_items(agent.inventory.items):
            try:
                nm = it.objs[0].name
            except Exception:
                nm = '?'
            foods.append(f"{nm}x{getattr(it, 'count', 1)}")
        print(f"t={t} inv={foods} corpses_below={[ (i.objs[0].name) for i in agent.inventory.items_below_me if i.is_corpse()]}",
              flush=True)
    if term or trunc:
        break
m = env.metrics()
print(json.dumps(dict(seed=a.seed, progress=m.progress, turns=m.turns, depth=m.max_depth,
                      milestone=m.milestone, cause=m.cause_of_death)))