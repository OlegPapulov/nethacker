import json, os, sys, importlib
tree = os.path.abspath(sys.argv[1]); seed = int(sys.argv[2]); maxt = int(sys.argv[3]) if len(sys.argv)>3 else 3000
sys.path.insert(0, tree)
from nethackers.arena.environment import make_environment
from nethackers.arena.seeds import trajectory_spec
import nethackers.contracts.models as models
spec = trajectory_spec("public", "local", seed)
env = make_environment(models.DEFAULT_MAX_STEPS, models.DEFAULT_NO_PROGRESS_TIMEOUT, character="wiz-hum-cha-mal")
obs = env.reset(spec)
bot_mod = importlib.import_module("bot")
ag = bot_mod.make_agent()
ag.reset(obs)
turns = 0
while True:
    act = ag.act(obs)
    obs, r, term, trunc = env.step(act)
    m = env.metrics(); turns = max(turns, m.turns)
    if m.turns > maxt or term or trunc: break
m = env.metrics()
print(json.dumps({"seed": seed, "progress": round(m.progress,4), "turns": turns, "depth": m.max_depth,
                  "cause": m.cause_of_death, "status": term or trunc}))
print("THREAD ERROR:\n", getattr(ag, "_driver").thread_error)
env.close()
