import argparse, importlib, os, sys, warnings, time, traceback
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")
from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh
p = argparse.ArgumentParser(); p.add_argument("--seed", type=int, default=4)
p.add_argument("--character", default="wiz-hum-cha-mal")
p.add_argument("--until", type=int, default=900); p.add_argument("--solution", default="/workspace")
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
it = agent.inventory.items
def snap():
    return dict(suit=it.suit and it.suit.objs[0].name, helm=it.helm and it.helm.objs[0].name,
                cloak=it.cloak and it.cloak.objs[0].name, mh=it.main_hand and it.main_hand.objs[0].name)
state = {'done': False, 'tries': 0}
orig = agent.direction
def direction(*args, **kwargs):
    r = orig(*args, **kwargs)
    if state['tries'] > 12:
        return r
    if agent.blstats.time >= a.until and getattr(agent, 'blstats', None) is not None:
        state['tries'] += 1
        state['done'] = True
        print("=== probe at t", agent.blstats.time, "xp", agent.blstats.experience_level,
              "energy", agent.blstats.energy, "/", agent.blstats.max_energy,
              "hunger", agent.blstats.hunger_state)
        print("known", agent.character.known_spells, "fail", agent.character.spell_fail_chance)
        print("worn", snap())
        mons = [m for m in agent.get_visible_monsters() if m[0] >= 1]
        print("mons", [(m[3].mname, int(m[1]), int(m[2]), int(m[0])) for m in mons][:6])
        try:
            for spell in ['force bolt']:
                mons = [m for m in agent.get_visible_monsters() if m[0] >= 2]
                if mons:
                    m = mons[0]
                    dy, dx = int(m[1]) - agent.blstats.y, int(m[2]) - agent.blstats.x
                else:
                    dy, dx = -1, 1
                before = (agent.blstats.time, agent.blstats.hitpoints, agent.blstats.energy)
                agent.cast(spell, direction=(dy, dx))
                agent.search(max_count=1)
                print(f"cast {spell} at ({dy},{dx}): msg={agent.message!r}")
                print("   before", before, "after",
                      (agent.blstats.time, agent.blstats.hitpoints, agent.blstats.energy),
                      "hunger", agent.blstats.hunger_state)
        except BaseException:
            traceback.print_exc()
    return r
agent.direction = direction
extra = 0
while True:
    act = bot.act(obs); obs, r, term, trunc = env.step(act)
    if term or trunc: break
    if state['done']:
        extra += 1
        if extra > 3: break
print("done")
