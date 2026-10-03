"""Trace the final turns of a seed: action, hp, hunger, message, surroundings."""
import argparse, collections, importlib, os, sys, warnings, time
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")
from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
from nethackers.arena.progress import NetHackProgress
import nle.nethack as nh

p = argparse.ArgumentParser()
p.add_argument("--seed", type=int, default=12)
p.add_argument("--character", default="wiz-hum-cha-mal")
p.add_argument("--tail", type=int, default=120)
p.add_argument("--max-turns", type=int, default=10 ** 9)
p.add_argument("--solution", default="/workspace")
a = p.parse_args()
sys.path.insert(0, a.solution)
bm = importlib.import_module("bot")
spec = trajectory_spec("public", "local", a.seed)
env = make_environment(1_000_000, 10_000, a.character)
bot = bm.make_agent(); obs = env.reset(spec); bot.reset(obs)
drv = bot._driver
for _ in range(600):
    agent = getattr(drv, "_agent", None)
    if agent is not None and getattr(agent, "blstats", None) is not None:
        break
    time.sleep(0.05)
prog = NetHackProgress()
TIME, HP, HPMAX, HUNGER, XP, DEPTH = (nh.NLE_BL_TIME, nh.NLE_BL_HP, nh.NLE_BL_HPMAX,
                                       nh.NLE_BL_HUNGER, nh.NLE_BL_XP, nh.NLE_BL_DEPTH)
ENERGY = 12
hist = collections.Counter()
ring = collections.deque(maxlen=a.tail)
mon_hist = collections.Counter()

steps = 0
while True:
    act = bot.act(obs)
    mons = None
    try:
        mons = [(m[0], int(m[1]), int(m[2]), m[3].mname) for m in agent.get_visible_monsters()]
    except BaseException:
        pass
    obs, _r, term, trunc = env.step(act)
    steps += 1
    prog.update(obs)
    bs = obs["blstats"]
    t = int(bs[TIME])
    hist[str(act) if isinstance(act, str) else ('act%d' % act)] += 1
    for _d, _y, _x, nm in (mons or []):
        mon_hist[nm] += 1
    try:
        msg = agent.message
    except BaseException:
        msg = ''
    ring.append((t, str(act), int(bs[HP]), int(bs[HPMAX]), int(bs[HUNGER]),
                 int(bs[XP]), int(bs[DEPTH]), int(bs[ENERGY]),
                 ' '.join(f"{nm}@{dy},{dx}" for _d, dy, dx, nm in (mons or [])), msg))
    if t > a.max_turns or term or trunc:
        break
print(f"seed {a.seed} steps={steps} t={t} progress={prog.progression:.4f} term={term} trunc={trunc}")
print("death message:", obs.get("death_message", None) or obs.get("end_status", None))
print("\naction histogram:", hist.most_common(12))
print("\nmonster sighting histogram:", mon_hist.most_common(12))
print("\n--- last turns ---")
for row in ring:
    t, act, hp, hpmax, hung, xp, depth, ene, mons, msg = row
    print(f"t={t} {act:<12} hp={hp:>3}/{hpmax:<3} hung={hung} xp={xp:>3} d={depth} ene={ene} | {mons[:60]:<60} | {msg[:70]}")
