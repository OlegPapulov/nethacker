"""Manual game control: play with the agent until a monster is adjacent, then take
over and cast force bolt by hand, recording energy cost, message and outcome.

Usage: python loop/probe_bolt3.py <tree> <seed>
"""
from __future__ import annotations

import os
import sys

import numpy as np

tree = os.path.abspath(sys.argv[1])
seed = int(sys.argv[2])
sys.path.insert(0, tree)

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nethackers.contracts.models as models
from nle.nethack import actions as A
from nle import nethack as nh
from autoascend import agent as aa_agent
from autoascend.glyph import G, MON
from autoascend import utils as uu

ACTIONS = tuple(nh.ACTIONS)


def act_int(action):
    if isinstance(action, str):
        return int(A.ACTIONS[A.ACTIONS.index(ord(action))])
    return int(action)


spec = trajectory_spec("public", "local", seed)
env = make_environment(models.DEFAULT_MAX_STEPS, models.DEFAULT_NO_PROGRESS_TIMEOUT,
                       character="wiz-hum-cha-mal")
obs = env.reset(spec)
import bot as bot_mod

bot = bot_mod.make_agent()
bot.reset(obs)
d = bot._driver
a = d._agent

turns = 0
target = None
while True:
    action = d.act(obs)
    obs, r, term, trunc = env.step(act_int(action))
    m = env.metrics()
    turns = max(turns, m.turns)
    if term or trunc or turns > 6000:
        print("episode over", term, trunc, turns, m.cause_of_death)
        break
    bl = obs["blstats"]
    py, px = int(bl[1]), int(bl[0])
    mask = uu.isin(obs["glyphs"], G.MONS)
    mask[py, px] = False
    ys, xs = np.nonzero(mask)
    if len(ys) and turns >= 400:
        i = int(np.argmin([abs(int(y) - py) + abs(int(x) - px) for y, x in zip(ys, xs)]))
        y, x = int(ys[i]), int(xs[i])
        target = (y, x, MON.permonst(obs["glyphs"][y, x]).mname, py, px, int(bl[14]))
        break

if target is None:
    print("no monster found")
    sys.exit(0)

d.close()
y, x, mname, py, px, energy = target
dy, dx = (y > py) - (y < py), (x > px) - (x < px)
key = {(1, 0): "s", (-1, 0): "n", (0, 1): "e", (0, -1): "w",
       (1, 1): "se", (1, -1): "sw", (-1, 1): "ne", (-1, -1): "nw"}[(dy, dx)]
print(f"turn={turns} target={mname} at ({y},{x}) self=({py},{px}) energy={energy} dir={key}")


def send(action, label=""):
    global obs
    obs, r, term, trunc = env.step(act_int(action))
    bl = obs["blstats"]
    msg = bytes(obs["message"]).decode(errors="replace").replace("\0", " ").strip()
    print(f"  [{label or action}] hp={bl[10]}/{bl[11]} en={bl[14]}/{bl[15]} t={bl[20]} tty_msg={msg[:80]!r} "
          f"misc={list(obs['misc'])}")
    return msg


def clear():
    for _ in range(6):
        if obs["misc"][2]:
            send(A.TextCharacters.SPACE, "SPACE")
        elif b"[yn]" in bytes(obs["tty_chars"].reshape(-1)):
            send("y", "yn")
        else:
            return


for _ in range(3):
    send(A.Command.ESC, "ESC")
clear()
send(A.Command.CAST, "CAST")
clear()
send("a", "letter a")
clear()
send(key, f"dir {key}")
clear()
g = obs["glyphs"][y, x]
print("  target glyph now:", int(g), MON.permonst(g).mname if MON.is_monster(g) else "(not a monster)")
env.close()
