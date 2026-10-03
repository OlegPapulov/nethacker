import argparse, importlib, os, sys, warnings, time
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")
from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh
p = argparse.ArgumentParser(); p.add_argument("--seed", type=int, default=0)
p.add_argument("--character", default="wiz-hum-cha-mal"); p.add_argument("--turns", type=int, default=100)
p.add_argument("--solution", default="/workspace"); a = p.parse_args()
sys.path.insert(0, a.solution)
bm = importlib.import_module("bot")
spec = trajectory_spec("public", "local", a.seed)
env = make_environment(1_000_000, 10_000, a.character)
bot = bm.make_agent(); obs = env.reset(spec); bot.reset(obs)
drv = bot._driver; agent = drv._agent
for _ in range(400):
    if agent is not None and getattr(agent, 'blstats', None) is not None: break
    time.sleep(0.05)
print("role", agent.character.role, "known_spells", agent.character.known_spells)
print("spell_level", agent.character.spell_level, "fail", agent.character.spell_fail_chance)
while True:
    act = bot.act(obs); obs, r, term, trunc = env.step(act)
    if term or trunc or int(obs["blstats"][nh.NLE_BL_TIME]) > a.turns: break
print("after", a.turns, "turns known_spells", agent.character.known_spells)
print("energy", agent.blstats.energy, "/", agent.blstats.max_energy, "hunger", agent.blstats.hunger_state)
print("messages tail:", agent.message)
