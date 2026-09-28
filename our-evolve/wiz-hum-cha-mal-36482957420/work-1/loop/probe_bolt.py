"""Measure force bolt: reach, hit rate and cost, by firing it instead of meleeing.

Hooks Agent.melee_attack (distance 1) and Agent.go_to (any distance) and fires
the spell instead, logging distance, message and whether the target survived.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

tree = os.path.abspath(sys.argv[1])
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
max_turns = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
sys.path.insert(0, tree)

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nethackers.contracts.models as models
from nle.nethack import actions as A
from autoascend import agent as aa_agent
from autoascend.character import Character

# known spells: parse the cast menu once at startup
orig_parse = Character.parse
state = {"known": {}, "log": Counter(), "cost": [], "n": 0, "miss": 0}


def parse(self):
    orig_parse(self)
    a = self.agent
    with a.atom_operation():
        a.step(A.Command.CAST)
        for line in a.popup:
            if ' - ' in line and 'force bolt' in line:
                state["known"]["force bolt"] = line.split(' - ')[0].strip()
        a.step(A.Command.ESC)
    self.known_spells = dict(state["known"])


Character.parse = parse

orig_melee = aa_agent.Agent.melee_attack
orig_go_to = aa_agent.Agent.go_to


def fire_bolt(self, y, x, tag):
    letter = state["known"].get("force bolt")
    if letter is None:
        return False
    dy, dx = y - self.blstats.y, x - self.blstats.x
    dis = max(abs(dy), abs(dx))
    if (dy, dx) == (0, 0):
        return False
    sy, sx = (0 if dy == 0 else (1 if dy > 0 else -1)), (0 if dx == 0 else (1 if dx > 0 else -1))
    energy_before = int(self.blstats.energy)
    self.cast("force bolt", direction=(sy, sx))
    msg = self.message[-90:]
    alive = int(self.glyphs[y, x]) if 0 <= y < 21 and 0 <= x < 79 else -1
    state["log"][(tag, dis, msg)] += 1
    state["n"] += 1
    if energy_before - int(self.blstats.energy) < 0:
        state["miss"] += 1
    return True


def melee(self, y, x):
    if fire_bolt(self, y, x, "melee"):
        return True
    return orig_melee(self, y, x)


def go_to(self, y, x, *a, **k):
    # if the destination is a monster tile further than 1 away, test the spell there
    if (y, x) != (self.blstats.y, self.blstats.x):
        from autoascend import utils as uu
        from autoascend.glyph import G
        if uu.isin(self.glyphs, G.MONS)[y, x]:
            fire_bolt(self, y, x, "goto")
    return orig_go_to(self, y, x, *a, **k)


aa_agent.Agent.melee_attack = melee
aa_agent.Agent.go_to = go_to

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
    if m.turns > max_turns or term or trunc:
        break
m = env.metrics()
print(f"known={state['known']} casts={state['n']} seed={seed} turns={turns} "
      f"progress={m.progress:.4f} cause={m.cause_of_death}")
for (tag, dis, msg), c in state["log"].most_common(25):
    print(f"  {c:>4}x {tag} dis={dis}: {msg!r}")
env.close()
