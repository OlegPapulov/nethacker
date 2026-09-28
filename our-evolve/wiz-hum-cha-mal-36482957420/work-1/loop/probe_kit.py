"""Dump the wizard's starting kit and known spells, via the real agent loop."""
from __future__ import annotations

import json
import os
import sys

tree = os.path.abspath(sys.argv[1])
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
max_turns = int(sys.argv[3]) if len(sys.argv) > 3 else 400
sys.path.insert(0, tree)

from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nethackers.contracts.models as models
from nle.nethack import actions as A
from autoascend import agent as aa_agent
from autoascend.character import Character

orig_parse = Character.parse


def parse(self):
    orig_parse(self)
    a = self.agent
    b = a.blstats
    print("character:", a.character)
    print("hp=%s/%s energy=%s max_energy=%s ac=%s str=%s dex=%s con=%s" % (
        b.hitpoints, b.max_hitpoints, b.energy, b.max_energy, b.armor_class,
        b.strength, b.dexterity, b.constitution))
    print("inv:")
    for i in a.inventory.items:
        for o in i.objs:
            print("   ", i.letter, repr(o.name), "qty", i.count, "cat", i.category,
                  "sub", o.sub, "wt", i.weight())
    with a.atom_operation():
        a.step(A.Command.CAST)
        print("CAST POPUP:")
        for line in a.popup:
            print("   ", repr(line))
        a.step(A.Command.ESC)


Character.parse = parse

orig_update = aa_agent.Agent.update
state = {"logged": set()}


def update(self, observation, additional_action_iterator=None):
    orig_update(self, observation, additional_action_iterator)
    b = getattr(self, "blstats", None)
    if b is None or b.experience_level > 3:
        return
    key = (int(b.experience_level), int(b.energy), int(b.max_energy))
    if key in state["logged"]:
        return
    state["logged"].add(key)
    print(f"t={b.time} XL{b.experience_level} energy={b.energy}/{b.max_energy} "
          f"hp={b.hitpoints}/{b.max_hitpoints} ac={b.armor_class} dlv={b.depth}")


aa_agent.Agent.update = update

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
env.close()
