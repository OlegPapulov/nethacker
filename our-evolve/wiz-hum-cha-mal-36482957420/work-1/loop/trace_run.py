"""Diagnostic trace of a bot run (local only; the arena sandbox cannot do this).

Usage: python loop/trace_run.py <tree_dir> <seed> [max_turns] [out.jsonl]
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import time

import numpy as np


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tree")
    p.add_argument("seed", type=int)
    p.add_argument("max_turns", type=int, default=60000)
    p.add_argument("out", nargs="?", default=None)
    args = p.parse_args()

    tree = os.path.abspath(args.tree)
    sys.path.insert(0, tree)
    os.environ["AA_TRACE"] = args.out or f"/workspace/loop/trace_{args.seed}.jsonl"

    from nethackers.arena.environment import make_environment
    from nethackers.arena.seeds import trajectory_spec
    import nethackers.contracts.models as models
    from autoascend import agent as aa_agent
    from autoascend.glyph import MON

    trace = open(os.environ["AA_TRACE"], "w")

    orig_update = aa_agent.Agent.update
    orig_fight2 = aa_agent.Agent.fight2
    orig_melee = aa_agent.Agent.melee_attack
    orig_fire = aa_agent.Agent.fire
    state = {"n_melee": 0, "n_fire": 0, "last_mon": None, "kills": 0}

    def rec(agent, kind, extra=None):
        if not hasattr(agent, "blstats"):
            return
        # NB: reading monsters through agent.get_visible_monsters()/agent.bfs()
        # here would populate the cached BFS and perturb the run. Use raw glyphs.
        from autoascend import utils as aa_utils
        from autoascend.glyph import G
        mons = []
        gy, gx = int(agent.blstats.y), int(agent.blstats.x)
        for y, x in zip(*aa_utils.isin(agent.glyphs, G.MONS).nonzero()):
            mons.append([abs(int(y) - gy) + abs(int(x) - gx), MON.permonst(agent.glyphs[y, x]).mname,
                         int(y), int(x)])
        mons.sort()
        row = {
            "t": int(agent.blstats.time), "kind": kind,
            "hp": int(agent.blstats.hitpoints), "mhp": int(agent.blstats.max_hitpoints),
            "en": int(agent.blstats.energy), "ac": int(agent.blstats.armor_class),
            "xl": int(agent.blstats.experience_level), "d": int(agent.blstats.depth),
            "dun": int(agent.blstats.dungeon_number), "lev": int(agent.blstats.level_number),
            "hunger": int(agent.blstats.hunger_state),
            "wpn": (agent.inventory.items.main_hand.objs[0].name
                    if getattr(agent.inventory.items, "main_hand", None) is not None else None),
            "arm": (agent.inventory.items.suit.objs[0].name
                    if getattr(agent.inventory.items, "suit", None) is not None else None),
            "mons": mons[:5],
            "step": int(agent.step_count),
        }
        if extra:
            row.update(extra)
        trace.write(json.dumps(row) + "\n")

    def update(self, observation, additional_action_iterator=None):
        before = getattr(self, "blstats", None)
        before_hp = before.hitpoints if before is not None else None
        orig_update(self, observation, additional_action_iterator)
        if hasattr(self, "blstats") and (before_hp is None or before_hp != self.blstats.hitpoints
                                         or state["n_melee"] or state["n_fire"]):
            rec(self, "step", {"hp_delta": (None if before_hp is None
                                            else int(before_hp - self.blstats.hitpoints))})

    def melee(self, y, x):
        try:
            g = self.glyphs[y, x]
            if MON.is_monster(g):
                state["last_mon"] = MON.permonst(g).mname
        except Exception:
            pass
        state["n_melee"] += 1
        ret = orig_melee(self, y, x)
        rec(self, "melee", {"mon": state["last_mon"]})
        state["n_melee"] = 0
        return ret

    def fire(self, item, direction):
        state["n_fire"] += 1
        rec(self, "fire", {"item": item.objs[0].name if item else None})
        return orig_fire(self, item, direction)

    aa_agent.Agent.update = update
    aa_agent.Agent.melee_attack = melee
    aa_agent.Agent.fire = fire

    spec = trajectory_spec("public", "local", args.seed)
    env = make_environment(models.DEFAULT_MAX_STEPS, models.DEFAULT_NO_PROGRESS_TIMEOUT,
                           character="wiz-hum-cha-mal")
    try:
        obs = env.reset(spec)
        bot_mod = importlib.import_module("bot")
        agent = bot_mod.make_agent()
        import random as _random
        _random.seed(0)
        np.random.seed(0)
        agent.reset(obs)
        t0 = time.time()
        turns = 0
        while True:
            action = agent.act(obs)
            obs, reward, terminated, truncated = env.step(action)
            m = env.metrics()
            turns = max(turns, m.turns)
            if m.turns > args.max_turns or terminated or truncated:
                break
        m = env.metrics()
        print(json.dumps({"seed": args.seed, "progress": m.progress, "turns": turns,
                          "depth": m.max_depth, "cause": m.cause_of_death,
                          "seconds": round(time.time() - t0, 1)}))
    finally:
        trace.close()
        env.close()


if __name__ == "__main__":
    main()
