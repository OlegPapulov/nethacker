import os, sys, time
sys.setrecursionlimit(100000)
import threading
threading.stack_size(512 * 1024 * 1024)
import gymnasium as gym
import nle  # noqa
from nle import nethack as nh

env = gym.make("NetHack-v0", max_episode_steps=100, options="wiz-hum-cha-mal")
obs, info = env.reset(seed=3)
print("PROGRAM_STATE", obs["program_state"] if "program_state" in obs else None)
bl = obs["blstats"]
print("dlevel", bl[nh.BL_DLEVEL], "hp", bl[nh.BL_HP])
print(obs["message"])
tty = obs["tty_chars"]
rows = [list(tty[i*80:(i+1)*80]) for i in range(24)]
for r in rows:
    print("|" + "".join(chr(c) if 32 <= c < 127 else " " for c in r) + "|")
env.close()
