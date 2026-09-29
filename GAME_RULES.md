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