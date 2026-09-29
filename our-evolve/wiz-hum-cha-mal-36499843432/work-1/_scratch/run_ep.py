"""Local batch episode runner mirroring the arena setup (wiz-hum-cha-mal)."""
import argparse
import json
import os
import sys
import time

sys.setrecursionlimit(100000)
import threading  # noqa

threading.stack_size(512 * 1024 * 1024)

os.environ.setdefault("XDG_CACHE_HOME", "/workspace/_scratch/cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/workspace/_scratch/cache/numba")

import gymnasium as gym
import nle  # noqa
import numpy as np
from nle import nethack as nh

sys.path.insert(0, "/workspace")


def run_seed(seed, max_turns, tag=""):
    from bot import make_agent

OBS_KEYS = ("glyphs", "chars", "colors", "specials", "blstats", "message", "inv_glyphs",
            "inv_strs", "inv_letters", "inv_oclasses", "screen_descriptions", "tty_chars",
            "tty_colors", "tty_cursor", "misc", "internal", "program_state")

OBS_KEYS = ("glyphs", "chars", "colors", "specials", "blstats", "message", "inv_glyphs",
            "inv_strs", "inv_letters", "inv_oclasses", "screen_descriptions", "tty_chars",
            "tty_colors", "tty_cursor", "misc", "internal", "program_state")


def run_seed(seed, max_turns, tag=""):
    from bot import make_agent

    env = gym.make("NetHack-v0", max_episode_steps=max_turns, character="wiz-hum-cha-mal",
                   observation_keys=OBS_KEYS, actions=tuple(nh.ACTIONS))
    env.unwrapped.seed(core=seed, disp=seed + 101, lgen=seed + 202, reseed=False)
    obs, _ = env.reset(seed=seed)
    agent = make_agent()
    agent.reset(obs)
    state = {"steps": 0, "obs": obs, "info": {}, "max_dlevel": int(obs["blstats"][nh.NLE_BL_DLEVEL]),
             "max_depth": int(obs["blstats"][nh.NLE_BL_DEPTH]), "max_xl": int(obs["blstats"][nh.NLE_BL_EXP]),
             "max_score": int(obs["blstats"][nh.NLE_BL_SCORE])}
    t0 = time.time()

    def run():
        obs = state["obs"]
        while state["steps"] < max_turns:
            action = agent.act(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            state["steps"] += 1
            state["info"] = info
            bl = obs["blstats"]
            state["max_dlevel"] = max(state["max_dlevel"], int(bl[nh.NLE_BL_DLEVEL]))
            state["max_depth"] = max(state["max_depth"], int(bl[nh.NLE_BL_DEPTH]))
            state["max_xl"] = max(state["max_xl"], int(bl[nh.NLE_BL_EXP]))
            state["max_score"] = max(state["max_score"], int(bl[nh.NLE_BL_SCORE]))
            if terminated or truncated:
                break

    t = threading.Thread(target=run)
    t.start()
    t.join()
    err = None
    if hasattr(agent, "_driver"):
        err = getattr(agent._driver, "thread_error", None)
    try:
        agent.close()
    except Exception:
        pass
    env.close()
    out = {
        "seed": seed,
        "steps": state["steps"],
        "max_dlevel": state["max_dlevel"],
        "max_depth": state["max_depth"],
        "max_xl": state["max_xl"],
        "max_score": state["max_score"],
        "end_status": str(state["info"].get("end_status")),
        "time": round(time.time() - t0, 1),
        "err": (err or "")[-3000:],
        "tag": tag,
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="0-14")
    ap.add_argument("--turns", type=int, default=30000)
    ap.add_argument("--out", default="")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    if "-" in a.seeds:
        lo, hi = a.seeds.split("-")
        seeds = list(range(int(lo), int(hi) + 1))
    else:
        seeds = [int(s) for s in a.seeds.split(",")]
    rows = []
    for s in seeds:
        r = run_seed(s, a.turns, a.tag)
        rows.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != "err"}), flush=True)
        if r["err"]:
            print("   ERR:", r["err"][-800:], flush=True)
    print("---- summary ----")
    print("mean depth", np.mean([r["max_depth"] for r in rows]),
          "mean dlevel", np.mean([r["max_dlevel"] for r in rows]),
          "mean xl", np.mean([r["max_xl"] for r in rows]),
          "mean steps", np.mean([r["steps"] for r in rows]))
    if a.out:
        with open(a.out, "w") as f:
            json.dump(rows, f, indent=1)


if __name__ == "__main__":
    main()
