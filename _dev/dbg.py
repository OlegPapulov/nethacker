"""Local debug harness: run one judge-namespace seed in-process and trace it."""
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--character", default="wiz-hum-cha-mal")
    p.add_argument("--trace", type=int, default=0, help="print every N turns")
    p.add_argument("--trace-from", type=int, default=0)
    p.add_argument("--max-turns", type=int, default=10 ** 9)
    p.add_argument("--solution", default="/workspace")
    a = p.parse_args()

    sys.path.insert(0, a.solution)
    bot_mod = importlib.import_module("bot")

    spec = trajectory_spec("public", "local", a.seed)
    env = make_environment(1_000_000, 10_000, a.character)
    bot = bot_mod.make_agent()
    obs = env.reset(spec)
    bot.reset(obs)
    started = time.time()
    steps = 0
    last_log = 0
    prog = NetHackProgress()
    bl_time = nh.NLE_BL_TIME
    while True:
        action = bot.act(obs)
        obs, _r, term, trunc = env.step(action)
        steps += 1
        prog.update(obs)
        t = int(obs["blstats"][bl_time])
        if a.trace and t >= a.trace_from and t - last_log >= a.trace:
            last_log = t
            bs = obs["blstats"]
            print(f"t={t} d={bs[nh.NLE_BL_DEPTH]} xp={bs[nh.NLE_BL_XP]} "
                  f"hp={bs[nh.NLE_BL_HP]}/{bs[nh.NLE_BL_HPMAX]} ac={bs[nh.NLE_BL_AC]} "
                  f"ene={bs[nh.NLE_BL_ENE]} hung={bs[nh.NLE_BL_HUNGER]} "
                  f"prog={prog.progression:.3f}", flush=True)
        if t > a.max_turns:
            break
        if term or trunc:
            break
    m = env.metrics()
    print(json.dumps(dict(seed=a.seed, progress=m.progress, turns=m.turns, max_depth=m.max_depth,
                          milestone=m.milestone, cause=m.cause_of_death, status=m.end_status,
                          steps=steps, wall=round(time.time() - started, 1))))
    drv = getattr(bot, "_driver", None)
    if drv is not None and drv._agent is not None:
        try:
            st = drv._agent.stats_logger.get_stats_dict()
            st = {k: v for k, v in st.items() if v}
            print("stats:", json.dumps({k: (round(v, 3) if isinstance(v, float) else v)
                                        for k, v in st.items()}))
        except Exception as e:
            print("stats err", e)
        try:
            print("panics:", [str(p.args[0])[:140] for p in drv._agent.all_panics[-6:]])
        except Exception:
            pass
    if drv is not None and drv.thread_error:
        print("thread_error:", drv.thread_error[-2000:])
    bot.close()
    env.close()


main()