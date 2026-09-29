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
## 2026-09-28 — wiz-hum-cha-mal: an HP threshold helps strong seeds and hurts weak ones

**Identity:** `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)
**Baseline:** packaged AutoAscend, 0.0624 · **Operator:** `opencode/big-pickle`, 19.9 M tokens

**Problem:**
The bot dies on dlvl 1 in 9 of 15 seeds. A natural reading of that is "it fights
when it should not". The operator's mutation acted on exactly that: it changed
**the hitpoint level at which the bot stops trying to win a fight**.

**Result: NOT-A-WIN.** 0.0650 vs 0.0624 on the mean — but per seed:

| direction | seeds |
|---|---|
| forward | **4, 9** |
| backward | **0, 2, 8, 11, 14** |
| deeper | **4** only |
| unchanged | 1, 3, 6, 7, 10, 12, 13, 15 (8 seeds) |

**Hypotheses for the next time:**
1. *It is a depth change, not a survival change.* Seed 4 — the **best** seed in
   the batch at 0.1791 — is the only one that got deeper (dlvl 7 → 8). If the
   threshold makes the bot disengage earlier, a strong game survives that and a
   doomed one just dies further from a fight it should have finished.
2. *The five backward seeds are all already-lost seeds.* Seeds 0, 2, 8, 11, 14
   score 0.021–0.075 and die on dlvl 1. Moving them "backward" may be noise on
   games that were lost either way.
3. *A single scalar cannot separate "retreat from a winnable fight" from
   "retreat from an unwinnable one".* The deciding variable is probably the
   monster, not the bot's own HP.

**Attempts:**
- Raise/lower the HP floor for engaging a fight → helps seed 4, hurts five seeds.
  Rejected by the paired test.

**Solution:** _pending — the current change is not kept._

**Notes:**
- The mean went **up** and the change was still rejected. That is the whole
  reason our loop judges per-seed: progression's SE over 15 seeds is 0.028, and
  this "improvement" was 0.0026.
- **19.9 M tokens / ~95 min** bought one rejected change. On a free tier that is
  the entire budget, so the brief may need to be shorter, or the instruction to
  make one change needs to be sharper.
- The operator **did** engage with our data — it proposed a specific HP threshold
  rather than "improve combat". The brief works.

## Experiments already run on this identity

## E1 — Establish a trustworthy baseline ◆ gameplay

**Identity:** `wiz-hum-cha-mal`
**Bot:** packaged `autoascend`, unmodified · **Operator:** none

**Question.** What does AutoAscend actually score here, on a machine that can
run it?

**Why this had to come first.** On an arm64 host this same tree scores **0.000
on all 15 seeds with `turns=0`** — the bot never starts, because `nltk` hangs
under emulation past the arena's 120-second startup guard. A zero obtained that
way is indistinguishable from a bad bot. Everything downstream would have been
reasoning about a measurement artifact.

**Result** (native x86_64 runner, run 36466145530):

```
published mean  0.0624      turn-1 deaths  0/15
validation mean 0.0579      turn-1 deaths  0/5
```

Zero startup deaths, so this is a genuine playing result. The champion for this
identity is **0.1907**, so there is 3.1× of headroom.

**10 of 15 seeds never leave dlvl 1** — to a goblin, a jackal, a bat, a kitten,
a newt, a hobbit, plus one grid bug and one starvation. Only five seeds get
past it, the best reaching dlvl 7.

**Caveat.** A mean over 15 seeds of this metric is a mixture of "dead on dlvl 1
at ~0.03" and "reached dlvl 5–7 at ~0.07–0.18", so it understates the good
seeds and overstates the bad ones. Per-seed rows, not the mean, drive
everything after this.

**Raises.** What is the loop's own baseline — the hub champion at 0.1907, or
this at 0.0624? Choosing the parent is the single highest-leverage decision
available, and it is not yet made.

---
## E4 — Building our own loop ✅ IT WORKS ◆ gameplay

**Identity:** `wiz-hum-cha-mal` · **Run:** 36482957420

**Question.** Can the operator be given what we have measured, using the
project's own mutator?

**The way in.** `ContainerOperator.run(worktree, brief: str)` takes the brief as
a **string**, so the mutator does not care where it came from. We compose it
ourselves and hand it over.

`loop/brief.py` builds the brief from:

1. **the measured baseline** — mean, per-seed table (turns, deepest, progress,
   died-of), and a depth histogram, because *"9 of 15 seeds never leave dlvl 1"*
   is a fact and *"0.0624"* is not;
2. **`experience.md` entries for this identity** — the observed failure modes,
   with attempts already ruled out;
3. **`experiments.md` entries for this identity**;
4. **the scoring rule that actually decides acceptance** — progression takes
   ~5 distinct values over 15 seeds, SE ≈ 0.028, and one seed can swing 0.18,
   so a positive mean is not evidence and a win needs most seeds forward;
5. **the contract**, verbatim, so it cannot be broken.

**Deliberately absent: any guess at the fix.** We know which seeds die and how;
we do not know the fix. A hint naming a fix is a hypothesis we have not tested,
and hypothesising is the one job worth delegating.

`loop/evolve.py` reuses the project's mutator, arena, seeding, image digests and
smoke gate **unchanged**. Only the brief is ours. Its paired verdict is
stricter than the stock loop's, and was unit-tested before any tokens were
spent:

```
5 seeds up, 0 down  -> WIN
3 seeds up, 2 down  -> NOT-A-WIN
unchanged           -> NOT-A-WIN
```

**Result — the brief reached the operator, and it used it.**

```
brief: 24,630 chars
operator: 19,889,701 tokens, completed
hypothesis: "the hitpoint level at which the bot stops trying to win a fight is …"

child 0.0650  vs  parent 0.0624
forward [4, 9]   backward [0, 2, 8, 11, 14]   deeper [4]   unchanged: 8 of 15
VERDICT NOT-A-WIN — only 2 seed(s) moved forward, below the 5 required
```

The hypothesis is a **specific mechanism**, not a platitude: the brief's data
invites exactly this question. For comparison, the stock loop's operator on the
same 0.0624 produced *"improved combat heuristics"* in general terms.

**The gate earned its keep.** The mean went **up** (0.0650 vs 0.0624) and the
change was still rejected: 2 forward, 5 backward. Progression's SE over 15 seeds
is 0.028; this "improvement" was 0.0026. **The stock loop's own logic would have
kept this candidate** — the paired test is the only thing between a 0.0026 mean
increase and a published regression.

**Caveats.**

- **19.9 M tokens and ~95 minutes** for one rejected change, which is the entire
  budget of a free tier.
- The hypothesis was **truncated mid-sentence** — the extraction regex captures
  one line, and the model wrote a multi-line rationale. Fixed in E6.
- 8 of 15 seeds were bit-identical, so the change was **narrower** than its
  hypothesis implies, and the seeds that moved mostly moved backwards.
- One identity, one seed, one operator, one iteration. Nothing generalises.

**Raises.**

1. **Seed 4 is the only seed that gained depth — and it is the batch's best
   seed** (0.1791, dlvl 7 → 8). All five regressions are already-lost seeds
   scoring 0.021–0.075. So the HP-threshold change is plausibly a **depth change
   wearing a survival hypothesis**: disengaging earlier helps a strong game and
   makes a doomed one die further from a fight it should have finished.
2. **19.9 M tokens is not a sustainable loop.** Either the brief is too long, or
   the model needs a tighter instruction to make *one* change rather than
   exploring.
3. **The stock loop would have kept a regression.** That is the strongest
   argument yet for running our own.

---

## The game itself

# Game rules — `wiz-hum-cha-mal`

Facts about the game, extracted from the NetHack source the arena
actually runs. Everything here is scoped to the deaths this bot
measured, because a general manual would be mostly irrelevant text.

**Source:** NetHack `NetHack-3.6.6_Released` — `src/monst.c`, `src/role.c`, `include/align.h`.
**Not** the wiki: `nethack.alt.org` is a parked domain and every guide
page 404s. The tagged C source is version-exact and does not change.

## The goal

Win NetHack: descend ~50 dungeon levels, take the Amulet of Yendor, and
escape through five planes. The arena scores *progress*, not a win:
BALROG progression in [0, 1], which rises as the bot survives, descends
and advances, pinned to a milestone ladder.

The ladder, measured on this identity's own seeds:

| depth | progression |
|---|---|
| dlvl 1 | ~0.03 |
| dlvl 2 | ~0.05 |
| dlvl 5 | ~0.075 |
| dlvl 7 | ~0.18 |
| dlvl 11 | ~0.16 |
| dlvl 19 | ~0.37 |
| dlvl 25 | ~0.47 |
| dlvl 28 | ~0.60 |

**This is the most important table in this file.** It says where the
score actually is. On this identity, 9 of 15 seeds never reach dlvl 1's
staircase, so the entire remaining game is worth about 0.03–0.05 and
nothing above it is reachable. A change that trades depth for safety
is the right trade *here* and a bad one in general.

## Who you are: wiz, hum, cha, mal

**Role** (`Wizard`, code `wiz`) — ability scores:

| Str | Int | Wis | Dex | Con | Cha |
|---|---|---|---|---|---|
| 7 | 10 | 7 | 7 | 7 | 7 |

Intelligence is your only strength. You start with almost no melee ability and must win at range or not at all — a point-blank fight with a jackal is one you will lose.

**Race** (`human`):

- hit points `2`

**Alignment** (`cha`) — from `include/align.h`:

- A_CHAOTIC = -1. You may use any weapon, and alignment only drifts you.
- Alignment is a hard *equipment* constraint, not a personality: a
  chaotic character is refused lawful-only items by the game itself.
- It does not gate ordinary combat, hunger, or movement — so for the
  early deaths below it is background, not a cause.

**Gender** (`mal`) — no mechanical effect in NetHack 3.6.6 beyond
dialogue flavour. Ignore it.

## What killed this bot, and what each killer actually is

Every row is a real death from the measured run, with the game's own
statistics for that creature. AC is the number that decides whether you
survive a hit; damage type decides whether armour helps at all.

| died to | seeds | lvl | AC | dmg | traits |
|---|---|---|---|---|---|
| wolf | 2 | 5 | 6 | PHYS | ANIMAL, NOHANDS, CARNIVORE |
| grid bug | 1 | 0 | 1 | ELEC | ANIMAL |
| hobbit | 1 | 1 | 2 | PHYS | HUMANOID, OMNIVORE |
| starvation | 1 | ? | ? | ? | *not parsed* |
| kitten | 1 | 2 | 3 | PHYS | ANIMAL, NOHANDS, CARNIVORE |
| newt | 1 | 0 | 1 | PHYS | SWIM, AMPHIBIOUS, ANIMAL |
| goblin | 1 | 0 | 1 | PHYS | HUMANOID, OMNIVORE |
| bat | 1 | 0 | 2 | PHYS | FLY, ANIMAL, NOHANDS |
| jackal | 1 | 0 | 1 | PHYS | ANIMAL, NOHANDS, CARNIVORE |
| white unicorn | 1 | 4 | 6 | PHYS | NOHANDS, HERBIVORE |
| crossbow bolt | 1 | ? | ? | ? | *not parsed* |
| soldier ant | 1 | 3 | 6 | PHYS | ANIMAL, NOHANDS, OVIPAROUS |
| rothe | 1 | 2 | 4 | PHYS | ANIMAL, NOHANDS, OMNIVORE |
| ape | 1 | 4 | 6 | PHYS | ANIMAL, HUMANOID, OMNIVORE |

### What this table says about the deaths

- **The killers are low-level but not harmless.** A goblin is level 0
  with AC 1, but it attacks with a weapon at 1d4. Against a level-0
  character with no armour that is a real fight, and there is no way to
  win it by trading blows.
- **The AC column is why fleeing works.** AC 1 means your hits almost
  always land; most of these creatures have low AC and hit often. The
  correct response to a fight you cannot finish is to not be in it.
- **`killer bee` deals DRST, not PHYS.** Armour does not reduce it. If a
  bee is the killer, AC is irrelevant and the only answer is distance.
- **`grid bug` deals ELEC and is level 0, AC 1.** It cannot be killed,
  cannot be outrun meaningfully, and there is no combat answer. The only
  correct play is to never step on it, which means detecting it from the
  glyph before moving.
- **`brown mold` deals COLD** and is stationary (M2_HOSTILE, level 1).
  Same lesson: do not touch it.
- **`soldier ant` is level 3 with AC 6** — the hardest killer in this
  table by a wide margin. It is also tiny (20 weight), so it is easy to
  walk into.

## Rules that decide whether you survive dlvl 1

These follow from the statistics above and from the game's own
mechanics, and they are the things a strategy change can act on.

1. **You cannot win a melee fight.** A level-0 wizard with no weapon
   skill loses to a goblin. Your damage output at level 0 is negligible
   against anything with more than 5 HP. Fight only what is already
   hurt, or do not fight.
2. **Disengage early, not at low HP.** The instinct to retreat when
   hurt is too late: several of these creatures hit for 1d6 or more, and
   a level-0 wizard has almost no HP to spend. The decision has to be
   made *before* HP matters, i.e. on the monster's state, not yours.
3. **Some monsters must never be engaged at all.** Grid bug (ELEC,
   unkillable), brown mold (COLD, stationary), and anything that
   attacks with a damage type your protection does not reduce.
4. **Retreat has to be geometrically possible.** A corridor with a
   monster behind you is not a retreat. Check the square you would move
   into before committing.
5. **Corpses are the only food on dlvl 1, and they rot.** A corpse is
   edible for roughly 50 turns, so a kill you walk away from is food
   you will not come back to. If you kill something, eat it then.
6. **Your own square is hidden.** The cell you stand on is drawn as the
   player glyph, so you cannot see a monster or item underfoot. A
   staircase is invisible while you occupy it, and so is a grid bug.
   You must remember what was there.

## What this file does not know

- Behaviour of the 68 identities not being played.
- Monster statistics for creatures this bot has not died to, though
  `src/monst.c` has all 393 and the generator can add them.
- Spell mechanics: casting costs, hunger per spell, and the damage
  numbers a level-0 wizard can actually produce. That is the largest
  gap, and it is the most likely place a real improvement lives —
  a wizard who can actually cast would not need any of rule 1 above.
- Anything about the bot's own code. That is in the brief.

---

Generated by `loop/build_game_rules.py` from NetHack `NetHack-3.6.6_Released`. Every
number above is parsed from that tag's source, not recalled. Regenerate
with `python loop/build_game_rules.py <identity> <diagnosis.json> GAME_RULES.md`.

These are the game's own numbers for the build you are playing, not approximations. Use them to decide whether a fight is winnable *before* you design the heuristic, rather than discovering afterwards that the fight was unwinnable.
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
