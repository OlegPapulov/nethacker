# Improving the NetHack bot for `wiz-hum-cha-mal`

You are improving a Python program that plays **NetHack** through the
**NetHack Learning Environment**. Make **one** focused change that
raises its score, and say why in a `# hypothesis:` comment.

## What has already been observed about this identity

These are measurements from previous runs. Attempts listed as
failed **have** been tried -- do not repeat them as if new.

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

## Experiments already run on this identity

## E1 — Establish the AutoAscend baseline on `wiz-hum-cha-mal`

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)
**Experience entry:** *wiz-hum-cha-mal: AutoAscend cannot start on this host*
**Bot under test:** packaged `autoascend`, unmodified
**Operator:** none (baseline only, no mutation)

**Question.**
What does AutoAscend actually score on this identity, measured on a machine
that can run it?

**Why this must come first.**
On this host the same tree scores **0.000 on all 15 seeds with `turns=0`** — the
bot never starts, because `nltk` hangs under arm64 emulation past the arena's
120-second startup guard. A zero obtained that way is indistinguishable from a
bad bot, and acting on it would be acting on a measurement artifact.

**Planned measurement.**
Run the packaged tree on the native x86_64 runner over the objective's own 15
published seeds, via the `diagnose` workflow already proven to work (it reports
per-seed turns, depth, progress and cause of death for both the published and a
reserved validation range).

**Result.** Measured on the native x86_64 runner (run 36466145530):

```
published mean  0.0624      turn-1 deaths  0/15
validation mean 0.0579      turn-1 deaths  0/5
```

Zero startup deaths, so this is a genuine playing result, not a harness artifact.

| | |
|---|---|
| baseline mean | **0.0624** |
| champion for this identity | **0.1907** (`daglar-dragomirov/bdf6eb25`) |
| headroom | **3.1x** |

**The failure mode is unambiguous — 10 of 15 seeds never leave dlvl 1:**

| dies on dlvl 1 (10) | reaches dlvl 2+ (5) |
|---|---|
| 0 goblin · 1 jackal · 3 **grid bug** · 5 bat · 6 **kitten** · 10 hobbit · 12 **newt** · 13 **starvation** · 14 **crossbow bolt** | 2 white unicorn (dl 5) · 4 wolf (dl 7) · 7 rothe (dl 2) · 8 soldier ant (dl 5) · 9 ape (dl 4) · 11 wolf (dl 5) |

Not one of those ten deaths is a boss or a clever trap. They are a **goblin**,
a **jackal**, a **bat**, a **kitten**, a **newt**, a **hobbit** — monsters a level-1
wizard should not lose to — plus one starvation and one crossbow bolt.

**Caveats.**
- The two *early* deaths (seed 3 at 3,052 turns to a grid bug; seed 13 at 5,206
  turns to starvation) suggest a second, distinct problem: the bot is spending
  its first several thousand turns in a place where it starves. That is not a
  combat problem and will not be fixed by a combat fix.
- `wiz-hum-cha-mal` is one identity, one parent, one operator. Nothing here
  generalises yet.
- The mean (0.0624) is a mixture of "dead on dlvl 1 at ~0.03" and "reached
  dlvl 5-7 at ~0.07-0.18", so it understates the seeds that do well and
  overstates the ones that die. Per-seed rows, not the mean, drive the next step.

**Raises.**
The obvious question is "why does a wizard lose to a goblin on dlvl 1", but the
per-seed table says the more precise question is **"which of the ten deaths are
the same bug?"** Seed 3's grid bug at 3,052 turns and seed 13's starvation at
5,206 turns are a different signature from seed 0's goblin at 13,697 turns.
Grouping the deaths before choosing a fix is the cheap next step and needs no
agent at all.

---

## How a change is judged

This is the part that is easy to get wrong, so read it carefully.

- `progress` is BALROG progression in [0, 1]: higher is better, and it rises as
  the bot survives, descends and advances.
- **The metric is coarse.** Across the 15 published seeds of a strong bot it
  takes only about **five distinct values**, because progression pins to
  milestone plateaus. Its standard error over 15 seeds is about **0.028**.
- Therefore a difference of means **cannot resolve a change of 0.01**, and any
  argument of the form "the average went up" is not evidence.
- A seed is a **complete, deterministic game**. So a change is judged **per
  seed**, candidate against parent, on the same seeds.
- **One seed can swing the score by 0.18.** So a change counts as an
  improvement only if **most seeds improve**, not if the average moved. In one
  real comparison a candidate gained +0.175 on one seed and lost -0.180 on
  another, and the mean of the two was +0.0013.
- Judge on **per-seed deltas and on the depth each seed reaches**, which is
  finer-grained than the progression value and is collected anyway.

## How to make your change

1. Make **one** focused change — a single idea, which may be a large diff.
2. Mark it with a `# hypothesis: ...` comment saying what you expect it to
   improve. The loop extracts that comment to attribute the change to you, and
   a change with no comment is recorded as unattributed.
3. Keep the contract working, and make sure the code imports cleanly.
4. **Do not tune to the seeds.** The seeds exist so changes are measured; a
   change that helps these 15 dungeons and nothing else will not transfer.
5. You have live Python and NLE. You may run a short foreground evaluation
   yourself to check the bot still works before you finish.

## The contract

- The bot lives at **`/workspace`**. Edit the strategy code in the
  `autoascend/` package, not the `arena_adapter.py` glue.
- `make_agent()` returns an object with `reset(observation)` and
  `act(observation) -> int`, where the int indexes `nle.nethack.ACTIONS`.
- Each episode is a fresh process, so all state lives on the instance.
- An exception, a bad action, or a timeout **zeroes that episode**, with no retry.
