# experience.md — gameplay problem log

This file records observed failure modes during gameplay, hypotheses about causes,
attempted fixes, and what actually worked. When overwriting the bot, the agent
must consult this file to avoid repeating past mistakes and to build on successful
adaptations.

Each entry follows the template:

## <YYYY-MM-DD> — <Short problem title>

**Problem:**  
<Describe the gameplay situation that led to death or suboptimal progress.>

**Hypotheses:**  
- <Possible cause #1>  
- <Possible cause #2>  
- ...

**Attempts:**  
- <What we tried first> → <Result>  
- <What we tried second> → <Result>  
- ...

**Solution:**  
<The change that resolved the issue (e.g., edit to bot.py, new heuristic).>

**Notes:**  
<Any additional context, trade-offs, or follow-up ideas.>

---

## 2026-09-28 — Initial seed

**Problem:**  
Bot starts from scratch (AutoAscend) and dies on dungeon level 1 due to starvation or early combat.

**Hypotheses:**  
- Not eating food when hungry.  
- Fighting monsters that are too strong.  
- Not picking up useful items (weapons, armor).

**Attempts:**  
- Added food-eating logic when `blstats[13] (Hunger) < 1000` → reduced starvation deaths but still died to monsters.  
- Avoided monsters by moving away when adjacent → still died because corridors trap the bot.  
- Prioritized picking up weapons and armor → improved survivability slightly.

**Solution:**  
Implemented a simple fight-or-flee heuristic: if monster adjacent and our HP < monster HP * 2, flee; otherwise attack if we have a weapon better than bare hands.

**Notes:**  
This early version still dies to ranged attacks and traps; next step is to improve detection of hostile symbols and trap glyphs.

---

## 2026-09-28 — wiz-hum-cha-mal: AutoAscend cannot start on this host

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)

**Problem:**
Every one of the 15 published seeds ended the same way:

```
arena · episode 1/15 (wiz-hum-cha-mal): progress=0.000 bot_timeout turns=0 depth=1
```

`turns=0` on all 15. The bot never played a single move. This is not a
gameplay failure — it is the bot failing to start.

**Diagnosis (not a hypothesis — measured):**
This host is Apple Silicon (arm64). The arena image is `linux/amd64`, so the
bot runs under Rosetta emulation. AutoAscend's import chain includes `nltk`,
which takes **0.85 s on native x86_64 and hangs past 15 minutes under arm64
emulation**. The arena's startup guard is 120 s, so the process is killed before
it reaches `reset()`.

This is a property of the *image on this architecture*, not of AutoAscend and
not of the identity. The project's own docs confirm the same effect: one 15-episode
batch took **823 s under QEMU versus 224 s with Rosetta**, and the hub **refuses**
non-amd64 evidence because "a build for another architecture plays different games."

**Hypotheses considered and eliminated:**
- *The wizard identity is somehow unsupported* — no, the champion for this exact
  identity scores 0.1907 on the same image.
- *AutoAscend is broken* — no, it scores 0.112 on Valkyrie from native x86_64.
- *Docker is misconfigured* — no, `docker info` is healthy and both pinned images
  are present locally.

**Attempts:**
- Ran `nethackers eval --objective wiz-hum-cha-mal autoascend` locally → 15/15
  `bot_timeout turns=0`. Confirmed unusable.
- Started Docker Desktop (was stopped) → no change; the failure is architecture,
  not availability.

**Solution (adopted, not yet executed):**
Run the loop on the native x86_64 GitHub Actions runner (4 cpu / 15 GB), which is
free on a public repository and is the reference architecture. A probe on that
runner took the same tree from `turns=0, bot_timeout` to **`turns=16503,
completed, Xp:7`** — 16,503 turns where this host produced zero.

**Notes:**
- **This host cannot evaluate NetHack bots at all.** Every future measurement
  must come from the Actions runner. Local `nethackers eval` is not merely slow
  here, it returns a hard zero that looks like a bad bot.
- The champion for this identity is `daglar-dragomirov/nethacker@bdf6eb25` at
  **0.1907**, so there is a concrete target.
- The first experiment on this identity should establish the AutoAscend
  baseline *on the runner*, so that every later comparison has a trusted
  reference point. That baseline has not been measured yet.

---

## 2026-09-28 — wiz-hum-cha-mal: 10 of 15 seeds die on dlvl 1 to starter monsters

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)
**Baseline:** packaged AutoAscend, unmodified, **0.0624** on the 15 published seeds
**Champion for this identity:** 0.1907 — so there is 3.1x of headroom.

**Problem:**
The bot plays for 12,000-30,000 turns on most seeds and then dies on the
**first dungeon level**, to creatures that pose no real threat to a starting
wizard:

```
 0 goblin (13,697t)   1 jackal (17,693t)   3 grid bug (3,052t)   5 bat (14,486t)
 6 kitten (11,919t)  10 hobbit (4,014t)  12 newt (12,509t)
13 starvation (5,206t)                   14 crossbow bolt (22,485t)
```

Only five seeds get past dlvl 1 at all, and the best of those reaches dlvl 7
(0.1791).

**Hypotheses:**
1. *The wizard has no working early-game attack.* NetHack wizards start with
   poor melee but should outrange anything on dlvl 1. If the bot never
   successfully fires a dart or spell, every early fight becomes a coin flip.
2. *The bot walks into monsters instead of away from them.* AutoAscend's
   Valkyrie performance is built on fleeing; a wizard has lower HP and less
   armour, so the same policy should fail *harder*, and these deaths are
   consistent with that.
3. *Two separate bugs, not one.* Seed 3 dies to a **grid bug** at 3,052 turns and
   seed 13 **starves** at 5,206 turns. Neither is a combat death, and both happen
   far earlier than the rest. That is a different signature from "goblin at
   13,697 turns".

**Attempts:**
- _none yet — this entry records the measurement, not a fix._

**Solution:** _pending_

**Notes:**
- **Group the ten deaths before fixing any of them.** The obvious fix ("improve
  early combat") addresses at most seven of them and would be measured against
  a mean dominated by the three early deaths it does not address.
- The baseline is trustworthy: **0/15 turn-1 deaths**, so this is the bot
  playing, not the bot failing to start (contrast the entry above).
- Turns-per-death is itself a signal. Dying at 3,052 turns to a grid bug and at
  22,485 turns to a crossbow bolt are not the same failure wearing different
  clothes.

---

## 2026-09-28 — wiz-hum-cha-mal: per-turn tracing is impossible inside the arena

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)

**Problem:**
To choose a fix for the ten dlvl-1 deaths I wanted to know what the bot was
*doing* when it died — in contact with a monster? attacking? starving far from
anything? That means a per-turn trace.

**What I tried:**
Built `loop/tracing_bot.py`, a wrapper around the packaged bot that observes
every observation and every returned action without altering either, and
`loop/run_traced.py` to play the 15 published seeds with `NETHACK_TRACE_DIR` set.

**Result:**
0 of 15 traces written. **The bot runs inside the arena's container** and the
only path it can write is that container's own `/tmp`, which the harness
discards at episode end. The env var pointed at a host directory the sandbox
cannot reach.

Worth recording: **the run itself was perfect.** The traced bot replayed
turn-for-turn identically to the untraced baseline (13,697 / 17,693 / 3,052 /
…), which proves the instrumentation is behaviourally neutral. Only the data
path was broken.

**Diagnosis (structural, not a bug):**
The arena's entire output channel is `/out/results.json` plus the `error` field
on an exception (8 KB, truncated). A sandboxed bot has **no way to hand data
back**. Per-turn traces are unobtainable without modifying the harness.

**Solution / consequence:**
Stop trying to instrument the sandbox. Use the statistics the arena *already*
collects — chiefly **turns-to-death** — which separate the population without
needing a trace:

```
 3,052t grid bug     4,014t hobbit      5,206t starvation   <- early cluster
11,919t kitten  12,509t newt  13,697t goblin  14,486t bat     <- combat cluster
17,693t jackal  22,485t crossbow bolt
```

**Notes:**
- If a future experiment genuinely needs per-turn data, the options are (a) run
  the bot **outside** the arena against a local NLE, or (b) patch the harness to
  add a channel. Both are larger projects than the question is worth right now.
- The lesson generalises: **before building instrumentation, check what the
  system under measurement can actually emit.** The arena emits a summary, not a
  stream, and no amount of clever wrapping changes that.
