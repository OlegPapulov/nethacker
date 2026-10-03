import argparse, importlib, os, sys, warnings, time
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")
from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh
p = argparse.ArgumentParser(); p.add_argument("--seed", type=int, default=4)
p.add_argument("--character", default="wiz-hum-cha-mal")
p.add_argument("--until", type=int, default=800); p.add_argument("--solution", default="/workspace")
a = p.parse_args()
sys.path.insert(0, a.solution)
bm = importlib.import_module("bot")
spec = trajectory_spec("public", "local", a.seed)
env = make_environment(1_000_000, 10_000, a.character)
bot = bm.make_agent(); obs = env.reset(spec); bot.reset(obs)
drv = bot._driver; agent = drv._agent
for _ in range(400):
    if agent is not None and getattr(agent, 'blstats', None) is not None: break
    time.sleep(0.05)
def snap():
    it = agent.inventory.items
    return dict(suit=it.suit and it.suit.objs[0].name, helm=it.helm and it.helm.objs[0].name,
                cloak=it.cloak and it.cloak.objs[0].name, gloves=it.gloves and it.gloves.objs[0].name,
                boots=it.boots and it.boots.objs[0].name, shirt=it.shirt and it.shirt.objs[0].name,
                mh=it.main_hand and it.main_hand.objs[0].name)
while True:
    act = bot.act(obs); obs, r, term, trunc = env.step(act)
    t = int(obs["blstats"][nh.NLE_BL_TIME])
    if term or trunc or t >= a.until: break
print("t", t, "known", agent.character.known_spells, "energy", agent.blstats.energy, agent.blstats.max_energy)
print("worn", snap())
mons = agent.get_visible_monsters()
print("monsters", [(m[3].mname, m[1], m[2], m[0]) for m in mons][:5])
mons = [m for m in mons if m[0] >= 2]
if mons:
    m = mons[0]
    dy, dx = int(m[1]) - agent.blstats.y, int(m[2]) - agent.blstats.x
    print("casting at", m[3].mname, dy, dx)
    agent.cast('force bolt', direction=(dy, dx))
    print("message:", repr(agent.message))
    print("popup:", agent.popup[:4])
    print("t after", agent.blstats.time, "hp", agent.blstats.hitpoints, "hunger", agent.blstats.hunger_state)
    print("energy", agent.blstats.energy)
else:
    print("no monster in range to cast at; casting blind NE")
    import traceback
    try:
        agent.cast('force bolt', direction=(-1, 1))
        print("message:", repr(agent.message))
        print("popup:", agent.popup[:4])
        print("t after", agent.blstats.time, "hp", agent.blstats.hitpoints, "hunger", agent.blstats.hunger_state)
    except BaseException as e:
        traceback.print_exc()
        print("THREAD ERR:", drv.thread_error[-1500:] if drv.thread_error else None)
