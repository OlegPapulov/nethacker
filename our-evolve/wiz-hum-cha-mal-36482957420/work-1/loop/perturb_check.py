"""Check whether instrumentation itself perturbs the run (sanity harness)."""
from __future__ import annotations

import json
import os
import sys

MODE = sys.argv[3] if len(sys.argv) > 3 else "none"

tree = os.path.abspath(sys.argv[1])
seed = int(sys.argv[2])
sys.path.insert(0, tree)

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nethackers.contracts.models as models
from autoascend import agent as aa_agent
from autoascend.glyph import MON

orig_update = aa_agent.Agent.update
orig_melee = aa_agent.Agent.melee_attack


def rec(agent):
    if MODE == "none":
        return
    from autoascend import utils as aa_utils
    from autoascend.glyph import G
    g = agent.glyphs
    for y, x in zip(*aa_utils.isin(g, G.MONS).nonzero()):
        _ = MON.permonst(g[y, x]).mname
    if MODE == "full":
        mh = getattr(agent.inventory.items, "main_hand", None)
        name = mh.objs[0].name if mh is not None else None
        _ = (agent.blstats.armor_class, agent.blstats.energy, name)


def update(self, observation, additional_action_iterator=None):
    orig_update(self, observation, additional_action_iterator)
    if hasattr(self, "blstats"):
        rec(self)


def melee(self, y, x):
    return orig_melee(self, y, x)


if MODE != "none":
    aa_agent.Agent.update = update
    aa_agent.Agent.melee_attack = melee

spec = trajectory_spec("public", "local", seed)
env = make_environment(models.DEFAULT_MAX_STEPS, models.DEFAULT_NO_PROGRESS_TIMEOUT,
                       character="wiz-hum-cha-mal")
obs = env.reset(spec)
import bot as bot_mod
agent = bot_mod.make_agent()
agent.reset(obs)
turns = 0
while True:
    action = agent.act(obs)
    obs, r, term, trunc = env.step(action)
    m = env.metrics()
    turns = max(turns, m.turns)
    if m.turns > 60000 or term or trunc:
        break
m = env.metrics()
print(json.dumps({"mode": MODE, "seed": seed, "progress": round(m.progress, 4), "turns": turns,
                  "depth": m.max_depth, "cause": m.cause_of_death}))
env.close()
