"""Run a set of judge seeds in-process and print a per-seed table + mean."""
import argparse
import importlib
import json
import os
import sys
import time
import warnings

os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")

from nethackers.arena.environment import make_environment
from nethackers.arena.progress import NetHackProgress
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh


def run_seed(seed, character, solution, keep_events=False):
    sys.path.insert(0, solution)
    bot_mod = importlib.import_module("bot")
    spec = trajectory_spec("public", "local", seed)
    env = make_environment(1_000_000, 10_000, character)
    bot = bot_mod.make_agent()
    obs = env.reset(spec)
    bot.reset(obs)
    steps = 0
    prog = NetHackProgress()
    xp_at = []
    started = time.time()
    while True:
        action = bot.act(obs)
        obs, _r, term, trunc = env.step(action)
        steps += 1
        prog.update(obs)
        xp = int(obs["blstats"][nh.NLE_BL_XP])
        if not xp_at or xp_at[-1][0] != xp:
            xp_at.append((xp, int(obs["blstats"][nh.NLE_BL_TIME])))
        if term or trunc:
            break
    m = env.metrics()
    drv = getattr(bot, "_driver", None)
    events = {}
    if drv is not None and drv._agent is not None:
        try:
            events = {k: int(v) for k, v in drv._agent.stats_logger.get_stats_dict().items() if v}
        except Exception:
            pass
    bot.close()
    env.close()
    return dict(seed=seed, progress=m.progress, turns=m.turns, depth=m.max_depth,
                milestone=m.milestone, cause=m.cause_of_death, wall=round(time.time() - started, 1),
                xp_curve=xp_at, events=events)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", default="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14")
    p.add_argument("--character", default="wiz-hum-cha-mal")
    p.add_argument("--solution", default="/workspace")
    p.add_argument("--events", action="store_true")
    a = p.parse_args()
    seeds = [int(s) for s in a.seeds.split(",") if s != ""]
    out = []
    for s in seeds:
        r = run_seed(s, a.character, a.solution)
        out.append(r)
        print(f"seed {r['seed']:>2} prog={r['progress']:.4f} {str(r['milestone']):>6} "
              f"turns={r['turns']:>6} depth={r['depth']:>2} {r['wall']:>5}s  {r['cause']}", flush=True)
        if a.events:
            print("      xp@turn:", r['xp_curve'])
            print("      events:", {k: v for k, v in sorted(r['events'].items()) if v})
    mean = sum(r["progress"] for r in out) / len(out)
    print(f"MEAN {mean:.4f} over {len(out)} seeds: {a.solution} seeds={a.seeds}")


main()