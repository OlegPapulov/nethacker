import argparse, importlib, os, sys, warnings, time, traceback
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")
from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh
p = argparse.ArgumentParser(); p.add_argument("--seed", type=int, default=4)
p.add_argument("--character", default="wiz-hum-cha-mal")
p.add_argument("--from-turn", type=int, default=300); p.add_argument("--casts", type=int, default=20)
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
it = agent.inventory.items
st = {'n': 0, 'started': False, 'armed': False, 'fails': 0, 'hits': 0, 'dmg': []}
orig = agent.direction
def direction(*args, **kwargs):
    r = orig(*args, **kwargs)
    if st['n'] >= a.casts:
        return r
    if not st['armed']:
        if agent.blstats.time >= a.from_turn:
            st['armed'] = True
            print("=== armed t", agent.blstats.time, "xp", agent.blstats.experience_level,
                  "energy", agent.blstats.energy, "/", agent.blstats.max_energy)
            print("known", agent.character.known_spells, "fail", agent.character.spell_fail_chance,
                  "levels", agent.character.spell_level)
            print("worn suit", it.suit and it.suit.objs[0].name, "helm", it.helm and it.helm.objs[0].name)
        return r
    if agent.blstats.energy < 5:
        return r
    mons = [m for m in agent.get_visible_monsters() if m[0] >= 2]
    if not mons:
        return r
    m = mons[0]
    dy, dx = int(m[1]) - agent.blstats.y, int(m[2]) - agent.blstats.x
    hp_before = int(agent.blstats.hitpoints)
    st['n'] += 1
    print(f"[{st['n']}] t={agent.blstats.time} xp={agent.blstats.experience_level} "
          f"ene={agent.blstats.energy} target={m[3].mname} d={m[0]} ac={m[3].ac} lvl={m[3].mlevel}",
          end=' ')
    try:
        agent.cast('force bolt', direction=(dy, dx))
        agent.search(max_count=1)
        msg = agent.message
        ok = 'fail to cast' not in msg
        st['hits' if ok else 'fails'] += 1
        print(f"-> {msg!r}")
    except BaseException:
        traceback.print_exc(); st['n'] = 10 ** 9
    return r
agent.direction = direction
n = 0
while n < 4000:
    act = bot.act(obs); obs, r, term, trunc = env.step(act); n += 1
    if term or trunc: break
print("casts", st['n'], "hits", st['hits'], "fails", st['fails'])
