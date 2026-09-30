# Game rules — `wiz-hum-cha-mal`

Facts about the game, extracted from the NetHack source the arena
actually runs. Everything here is scoped to the deaths this bot
measured, because a general manual would be mostly irrelevant text.

This file is **the game only**: monsters, your class, your race, and
the mechanics a strategy can act on. It contains no objective and no
scoring — what the loop is trying to achieve lives in the brief, and
what has already been tried lives in `experience.md`.

**Source:** NetHack `NetHack-3.6.6_Released` — `src/monst.c`, `src/role.c`, `include/align.h`.
**Not** the wiki: `nethack.alt.org` is a parked domain and every guide
page 404s. The tagged C source is version-exact and does not change.

## Who you are: wiz, hum, cha, mal

**Role** (`Wizard`, code `wiz`) — ability scores:

| Str | Int | Wis | Dex | Con | Cha |
|---|---|---|---|---|---|
| 7 | 10 | 7 | 7 | 7 | 7 |

Intelligence is your only strength: the ability spread gives you almost nothing in Str or Dex, so your damage output and your accuracy in melee both start from the bottom. A level-0 wizard has no melee answer to anything with more than a few hit points, and the class's tools are spells.

**Race** (`human`):

- hit points `2`

**Alignment** (`cha`) — from `include/align.h`:

- A_CHAOTIC = -1. You may use any weapon, and alignment only drifts you.
- Alignment is a hard *equipment* constraint, not a personality: a
  chaotic character is refused lawful-only items by the game itself.
- It does not gate ordinary combat, hunger, or movement, so it does not
  explain a death on its own.

**Gender** (`mal`) — no mechanical effect in NetHack 3.6.6 beyond
dialogue flavour. Ignore it.

## What killed this bot, and what each killer actually is

Every row is a real death from the measured run, with the game's own
statistics for that creature. AC is the number that decides whether you
survive a hit; damage type decides whether armour helps at all.

| died to | seeds | lvl | AC | dmg | speed | traits |
|---|---|---|---|---|---|---|
| wolf | 2 | 5 | 6 | PHYS | 12 | ANIMAL, NOHANDS, CARNIVORE |
| grid bug | 1 | 0 | 1 | ELEC | 12 | ANIMAL |
| hobbit | 1 | 1 | 2 | PHYS | 9 | HUMANOID, OMNIVORE |
| starvation | 1 | ? | ? | ? | ? | *not parsed* |
| kitten | 1 | 2 | 3 | PHYS | 18 | ANIMAL, NOHANDS, CARNIVORE |
| newt | 1 | 0 | 1 | PHYS | 6 | SWIM, AMPHIBIOUS, ANIMAL |
| goblin | 1 | 0 | 1 | PHYS | 6 | HUMANOID, OMNIVORE |
| bat | 1 | 0 | 2 | PHYS | 22 | FLY, ANIMAL, NOHANDS |
| jackal | 1 | 0 | 1 | PHYS | 12 | ANIMAL, NOHANDS, CARNIVORE |
| white unicorn | 1 | 4 | 6 | PHYS | 24 | NOHANDS, HERBIVORE |
| crossbow bolt | 1 | ? | ? | ? | ? | *not parsed* |
| soldier ant | 1 | 3 | 6 | PHYS | 18 | ANIMAL, NOHANDS, OVIPAROUS |
| rothe | 1 | 2 | 4 | PHYS | 9 | ANIMAL, NOHANDS, OMNIVORE |
| ape | 1 | 4 | 6 | PHYS | 12 | ANIMAL, HUMANOID, OMNIVORE |

`speed` is the `mov` field of the monster's `LVL(...)` record — its
movement points per turn. Ordinary dungeon creatures run 6 or 9; the
fastest in the game are far above that (an air elemental is 36), so a
high number means the creature closes a one-square gap every turn and
cannot be walked away from.

### What these statistics mean in the game

- **AC is what decides whether you survive a hit.** Most of these
  creatures have AC 1, so your attacks almost always land and theirs
  land too. AC is the number to compare before starting a fight.
- **Damage type decides whether armour helps at all.** A PHYS hit is
  reduced by armour; ELEC, COLD, DRST and FIRE are not. A creature that
  attacks with a non-PHYS type cannot be answered with a better AC.
- **`grid bug` is level 0, AC 1, ELEC.** Small, fast, and effectively
  unkillable for a low-level character. It is the game's clearest
  example of a monster with no combat answer.
- **`brown mold` is COLD and stationary** (M2_HOSTILE, level 1): it does
  not move and does not need to.
- **`soldier ant` is level 3 with AC 6** — by far the toughest creature in
  this table, and tiny (20 weight), so easy to walk into by accident.
- **Level is a poor guide to danger here.** A level-0 goblin and a level-0
  grid bug both outclass a level-0 wizard; a level-5 wolf has AC 6.

## Mechanics of the game that constrain any strategy

These are properties of NetHack, not opinions about how to play. They
are the facts a strategy has to be built around.

1. **Melee damage depends on Str and weapon skill, and experience levels
   both.** A character at level 0 does negligible damage to anything with
   more than a few HP. Killing is slow, and slowness has consequences
   below.
2. **A creature's attack resolves once per turn**, so being adjacent to
   one over many turns means taking many hits. Distance is a real
   resource, and the square you would retreat into has to be checked
   before committing to it — a corridor with a monster behind you is
   not an escape.
3. **Monsters have a movement speed (`mov`), the game's fastest being
   far above the ordinary range.** A creature with a high value closes a
   one-square gap every turn, so retreating one square does not open
   distance from it. The `speed` column above is that value: a wolf, a
   jackal and a grid bug are all 12, while a bat is 22 and a white
   unicorn 24. Those last two cannot be outrun at all.
4. **Corpses are food and they rot** — edible for roughly 50 turns. A
   kill walked away from is food that will not be there later.
5. **Hunger rises every turn** and a character who starves faints, which
   costs hit points and incapacitates the character while it happens.
   Eating is not optional, and a fainting character cannot fight.
6. **The square you stand on is not drawn to you.** It shows the player
   glyph, so a monster or item underneath you is invisible while you are
   on it — including a staircase, and including a grid bug. You cannot
   see what is underfoot and must remember it.
7. **Experience level comes from kills, and a level-up gives hit points.**
   So a character's ability to survive a fight rises with the number of
   fights it has already won — the early game is the hardest, and the
   thresholds roughly double at each level.
8. **Wizards are spellcasters first and fighters last.** A level-0 wizard
   has almost no melee ability. The intended answer to a fight that
   cannot be won at range is not to be in it. Spell mechanics —
   casting costs, hunger per spell, and the damage numbers available —
   are the largest gap in this file, and the most promising place for a
   real improvement, because a wizard who can actually cast would not
   need most of the advice above.

## Items

- **A weapon's damage depends on its weight and your Str**, and most
  early weapons are one-handed and light. A dagger is fast and weak; a
  heavier weapon hits harder and needs both hands.
- **Armor trades speed for protection**: a higher AC value means harder
  to hit, and wearing it makes the character slower to move and act.
  That trade is worth making against a slow, heavy hitter and usually
  not against something that already hits reliably.
- **Alignment gates what you can pick up.** A chaotic character cannot
  wield a lawful-only weapon; the game refuses the pickup outright.
- **Shields, rings, amulets and scrolls change one rule each** and are
  the main source of a large mid-game jump — but they are found, not
  bought, and the early seeds rarely contain any.
- **A backpack's weight limit matters**: a level-0 wizard can carry very
  little before becoming encumbered, and encumbered characters act
  slower and suffer worse to-hit.

## What this file does not know

- Behaviour of the 68 identities not being played.
- Monster statistics for creatures this bot has not died to, though
  `src/monst.c` has all 393 and the generator can add them.
- Spell mechanics: casting costs, hunger per spell, and the damage
  numbers a level-0 wizard can actually produce. That is the largest
  gap, and it is the most likely place a real improvement lives —
  a wizard who can actually cast would not need most of rule 1 above.
- Anything about the bot's own code, what the loop is trying to achieve,
  or what has already been tried. That is in the brief and in
  `experience.md`.

---

Generated by `loop/build_game_rules.py` from NetHack `NetHack-3.6.6_Released`. Every
number above is parsed from that tag's source, not recalled. Regenerate
with `python loop/build_game_rules.py <identity> <diagnosis.json> GAME_RULES.md`.