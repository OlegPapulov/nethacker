"""Measure force bolt reach/hit-rate by firing it wherever the bot would melee."""
import os, sys, traceback
from collections import Counter

tree = os.path.abspath(sys.argv[1]); seed = int(sys.argv[2]); max_turns = int(sys.argv[3])
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
    with a.atom_operation():
        a.step(A.Command.CAST)
        self.known_spells = {}
        for line in a.popup:
            if ' - ' in line and 'force bolt' in line:
                self.known_spells['force bolt'] = line.split(' - ')[0].strip()
        a.step(A.Command.ESC)
Character.parse = parse

stats = Counter()
orig_melee = aa_agent.Agent.melee_attack
def melee(self, y, x):
    letter = self.character.known_spells.get('force bolt')
    if letter is None:
        return orig_melee(self, y, x)
    dy, dx = int(y) - int(self.blstats.y), int(x) - int(self.blstats.x)
    en = int(self.blstats.energy)
    self.cast('force bolt', direction=((dy > 0) - (dy < 0), (dx > 0) - (dx < 0)))
    msg = self.message.replace('\n', ' ')[-70:]
    spent = en - int(self.blstats.energy)
    stats[f"en_spent={spent} | {msg}"] += 1
    return True
aa_agent.Agent.melee_attack = melee

spec = trajectory_spec('public', 'local', seed)
env = make_environment(models.DEFAULT_MAX_STEPS, models.DEFAULT_NO_PROGRESS_TIMEOUT,
                       character='wiz-hum-cha-mal')
obs = env.reset(spec)
import bot as bot_mod
agent = bot_mod.make_agent()
agent.reset(obs)
turns = 0
while True:
    a = agent.act(obs)
    obs, r, term, trunc = env.step(a)
    m = env.metrics(); turns = max(turns, m.turns)
    if m.turns > max_turns or term or trunc: break
m = env.metrics()
print(f"seed={seed} turns={turns} xl_prog={m.progress:.4f} cause={m.cause_of_death} casts={sum(stats.values())}")
for msg, c in stats.most_common(15):
    print(f"  {c:>4}x {msg}")
env.close()
