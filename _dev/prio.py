"""Record fight2 action priorities (melee/ranged vs best move) for the final turns of a seed."""
import argparse, importlib, os, sys, warnings, time
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/nethack_cache/xdg")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nethack_cache/numba")
warnings.filterwarnings("ignore")
from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nle.nethack as nh

p = argparse.ArgumentParser()
p.add_argument("--seed", type=int, default=12)
p.add_argument("--character", default="wiz-hum-cha-mal")
p.add_argument("--from-turn", type=int, default=4800)
p.add_argument("--max-print", type=int, default=20)
p.add_argument("--adjacent-only", action="store_true")
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
import autoascend.combat.fight_heur as fh
from autoascend.utils import adjacent
orig_get = fh.get_priorities
log = []
def get_priorities(ag):
    hm, acts = orig_get(ag)
    dis = ag.bfs()
    mv = fh.get_move_actions(ag, dis, hm)
    allacts = list(acts) + list(mv)
    mons = ag.get_visible_monsters()
    t = int(ag.blstats.time) if hasattr(ag.blstats, 'time') else -1
    if t < 0:
        t = log[-1][0] + 1 if log else 0
    adj = [m[3].mname for m in mons if adjacent((int(m[1]), int(m[2])), (int(ag.blstats.y), int(ag.blstats.x)))]
    try:
        pass
    except BaseException:
        pass
    if t >= a.from_turn and (not a.adjacent_only or adj):
        best = max(allacts, key=lambda x: x[0]) if allacts else None
        top = sorted(allacts, key=lambda x: -x[0])[:5]
        log.append((t, int(ag.blstats.hitpoints), int(ag.blstats.hunger_state)
                   if hasattr(ag.blstats, 'hunger_state') else -1,
                   [(m[3].mname, int(m[0]), int(m[1]), int(m[2]), int(m[3].ac), int(m[3].mmove)) for m in mons],
                   adj, [(round(pr, 1), ac[0] + str(tuple(ac[1:])[:2])) for pr, ac in top],
                   (round(best[0], 1), best[1][0]) if best else None))
    return hm, acts
fh.get_priorities = get_priorities
n = 0
while n < 200000:
    act = bot.act(obs); obs, _r, term, trunc = env.step(act); n += 1
    if term or trunc:
        break
seen = set()
for row in log[-a.max_print:]:
    t, hp, hung, mons, adj, top, best = row
    print(f"t={t} hp={hp} hung={hung} adj={adj} best={best}")
    print(f"    mons={mons}")
    print(f"    top={top}")
