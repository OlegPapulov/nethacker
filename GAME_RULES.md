# Game rules — `wiz-hum-cha-mal`

Facts about the game, extracted from the NetHack source the arena
actually runs. Everything here is scoped to what a character at this
starting level actually meets, because a general manual would be mostly
irrelevant text.

This file is **the game only**: monsters, your class, your race, and
the mechanics a strategy can act on. It contains no objective, no
scoring, and **no measurements** — what the loop is trying to achieve
lives in the brief, and what has already been tried lives in
`experience.md`. Nothing below says how often anything happened, and
that is deliberate: the only sample available is 15 published seeds,
which are not the dungeons this bot is ultimately scored on, so a
strategy shaped by them is tuned to the wrong game.

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

## The creatures of level 2 and below

Every creature in `src/monst.c` at level 2 or lower — the band a starting character meets on the
first dungeon levels — with the game's own statistics for each, ordered
by level and then hardest-first by AC.

| creature | lvl | AC | dmg | speed | wt | traits |
|---|---|---|---|---|---|---|
| bat | 0 | 2 | PHYS | 22 | 20 | FLY, ANIMAL, NOHANDS |
| human | 0 | 2 | PHYS | 12 | ? | HUMANOID, OMNIVORE |
| fox | 0 | 1 | PHYS | 15 | 300 | ANIMAL, NOHANDS, CARNIVORE |
| goblin | 0 | 1 | PHYS | 6 | 400 | HUMANOID, OMNIVORE |
| grid bug | 0 | 1 | ELEC | 12 | 15 | ANIMAL |
| jackal | 0 | 1 | PHYS | 12 | 300 | ANIMAL, NOHANDS, CARNIVORE |
| kobold | 0 | 1 | PHYS | 6 | 400 | HUMANOID, POIS, OMNIVORE |
| kobold zombie | 0 | 1 | PHYS | 6 | 400 | BREATHLESS, MINDLESS, HUMANOID |
| lichen | 0 | 1 | STCK | 1 | 20 | BREATHLESS, NOEYES, NOLIMBS |
| long worm tail | 0 | 1 | ? | 0 | 0 | - |
| newt | 0 | 1 | PHYS | 6 | 10 | SWIM, AMPHIBIOUS, ANIMAL |
| sewer rat | 0 | 1 | PHYS | 12 | 20 | ANIMAL, NOHANDS, CARNIVORE |
| killer bee | 1 | 5 | DRST | 18 | 1 | ANIMAL, FLY, NOHANDS |
| Keystone Kop | 1 | 3 | PHYS | 6 | ? | HUMANOID |
| cave spider | 1 | 3 | PHYS | 12 | 50 | CONCEAL, ANIMAL, NOHANDS |
| garter snake | 1 | 3 | PHYS | 8 | 50 | SWIM, CONCEAL, NOLIMBS |
| gnome | 1 | 3 | PHYS | 6 | 650 | HUMANOID, OMNIVORE |
| hobgoblin | 1 | 3 | PHYS | 9 | 1000 | HUMANOID, OMNIVORE |
| manes | 1 | 3 | PHYS | 3 | 100 | POIS |
| orc | 1 | 3 | PHYS | 9 | 850 | HUMANOID, OMNIVORE |
| acid blob | 1 | 2 | ACID | 3 | 30 | BREATHLESS, AMORPHOUS, NOEYES |
| brown mold | 1 | 2 | COLD | 0 | 50 | BREATHLESS, NOEYES, NOLIMBS |
| coyote | 1 | 2 | PHYS | 12 | 300 | ANIMAL, NOHANDS, CARNIVORE |
| gas spore | 1 | 2 | PHYS | 3 | 10 | FLY, BREATHLESS, NOLIMBS |
| gecko | 1 | 2 | PHYS | 6 | 10 | ANIMAL, NOHANDS, CARNIVORE |
| giant rat | 1 | 2 | PHYS | 10 | 30 | ANIMAL, NOHANDS, CARNIVORE |
| gnome zombie | 1 | 2 | PHYS | 6 | 650 | BREATHLESS, MINDLESS, HUMANOID |
| green mold | 1 | 2 | ACID | 0 | 50 | BREATHLESS, NOEYES, NOLIMBS |
| hobbit | 1 | 2 | PHYS | 9 | 500 | HUMANOID, OMNIVORE |
| large kobold | 1 | 2 | PHYS | 6 | 450 | HUMANOID, POIS, OMNIVORE |
| red mold | 1 | 2 | FIRE | 0 | 50 | BREATHLESS, NOEYES, NOLIMBS |
| yellow mold | 1 | 2 | STUN | 0 | 50 | BREATHLESS, NOEYES, NOLIMBS |
| Kop Sergeant | 2 | 4 | PHYS | 8 | ? | HUMANOID |
| centipede | 2 | 4 | DRST | 4 | 50 | CONCEAL, ANIMAL, NOHANDS |
| dwarf | 2 | 4 | PHYS | 6 | 900 | TUNNEL, NEEDPICK, HUMANOID |
| giant ant | 2 | 4 | PHYS | 18 | 10 | ANIMAL, NOHANDS, OVIPAROUS |
| hill orc | 2 | 4 | PHYS | 9 | 1000 | HUMANOID, OMNIVORE |
| kobold shaman | 2 | 4 | SPEL | 6 | 450 | HUMANOID, POIS, OMNIVORE |
| monkey | 2 | 4 | SITM | 12 | 100 | ANIMAL, HUMANOID, OMNIVORE |
| rabid rat | 2 | 4 | DRCO | 12 | 30 | ANIMAL, NOHANDS, POIS |
| rothe | 2 | 4 | PHYS | 9 | 400 | ANIMAL, NOHANDS, OMNIVORE |
| dwarf zombie | 2 | 3 | PHYS | 6 | 900 | BREATHLESS, MINDLESS, HUMANOID |
| floating eye | 2 | 3 | PLYS | 1 | 10 | FLY, AMPHIBIOUS, NOLIMBS |
| giant bat | 2 | 3 | PHYS | 22 | 30 | FLY, ANIMAL, NOHANDS |
| homunculus | 2 | 3 | SLEE | 12 | 60 | FLY, POIS |
| iguana | 2 | 3 | PHYS | 6 | 30 | ANIMAL, NOHANDS, CARNIVORE |
| kitten | 2 | 3 | PHYS | 18 | 150 | ANIMAL, NOHANDS, CARNIVORE |
| kobold lord | 2 | 3 | PHYS | 6 | 500 | HUMANOID, POIS, OMNIVORE |
| little dog | 2 | 3 | PHYS | 18 | 150 | ANIMAL, NOHANDS, CARNIVORE |
| orc zombie | 2 | 3 | PHYS | 6 | 850 | BREATHLESS, MINDLESS, HUMANOID |
| werejackal | 2 | 3 | PHYS | 12 | ? | HUMANOID, POIS, REGEN |
| wererat | 2 | 3 | PHYS | 12 | ? | HUMANOID, POIS, REGEN |

`speed` is the `mov` field of the monster's `LVL(...)` record — its
movement points per turn. Ordinary dungeon creatures run 6 or 9; the
fastest in the game are far above that (an air elemental is 36), so a
high number means the creature closes a one-square gap every turn and
cannot be walked away from.

### How to read those numbers

- **AC is what decides whether you survive a hit.** AC 1 means your
  attacks almost always land and theirs land too, so a fight is decided
  by turns taken rather than by luck. Compare AC before starting, not
  after.
- **Damage type decides whether armour helps at all.** A PHYS hit is
  reduced by armour; ELEC, COLD, DRST, FIRE, ACID and the rest are not.
  Most of this band attacks PHYS, but not most of it — a grid bug is
  ELEC and a centipede is DRST, and neither can be answered with a
  better AC.
- **`killer bee` is AC 5** and is the hardest creature in the band, at
  level 1. Nine more sit at AC 4, all level 2: `centipede`, `dwarf`,
  `giant ant`, `hill orc`, `kobold shaman`, `Kop Sergeant`, `monkey`,
  `rabid rat` and `rothe`. Nothing in the band is tougher than that.
- **`grid bug` is level 0, AC 1, ELEC, and speed 12.** It is the
  clearest example in the game of a monster with no combat answer at
  this level: fast enough to reach you, and nothing you do to AC or
  damage output changes that.
- **`bat` and `giant bat` run at speed 22**, `fox` at 15, and
  `killer bee`, `giant ant` and `kitten` at 18. Ordinary creatures run
  6 or 9. Against anything above 12, stepping back one square buys
  nothing.
- **The molds never move.** `brown mold`, `green mold`, `red mold` and
  `yellow mold` have speed 0 and are M2_HOSTILE: they do not need to
  chase you, and they are COLD, ACID, FIRE and STUN respectively, so
  armour does nothing for any of them.
- **Small does not mean harmless, and here it is literal.**
  `killer bee` weighs 1 and is AC 5 — the hardest creature in the band
  is also one of the smallest. `giant ant`, `newt`, `gecko` and
  `floating eye` are 10, `grid bug` 15, and `bat`, `lichen` and
  `sewer rat` 20. Every one of those is lighter than most pieces of
  equipment, so the creatures easiest to walk into by accident are the
  ones least likely to be noticed doing it.
- **`NOHANDS` creatures cannot wield a weapon**, and the
  `NOEYES`/`NOLIMBS`/`BREATHLESS` group — the molds, `lichen`,
  `acid blob`, `gas spore` — has no hands at all and cannot be reasoned
  about as an armed opponent.
- **`FLY` means it crosses what you cannot.** `bat`, `giant bat`,
  `killer bee`, `floating eye`, `gas spore` and `homunculus` pass over
  water and gaps that stop a walking character.
- **`werejackal` and `wererat` have REGEN.** Damage you do does not
  stay done, so an attrition plan that works on an ordinary creature of
  the same level does not work on a lycanthrope. `kobold shaman` attacks
  with SPEL rather than a physical blow, for the same reason: some
  things in this band cannot be answered the ordinary way.
- **Level is a poor guide to danger here.** A level-0 goblin and a
  level-0 grid bug both outclass a level-0 wizard, and the toughest
  creature in the band is a level 1.

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
   distance from it. The `speed` column above is that value: a goblin and
   a kobold run 6, a jackal and a grid bug run 12, and a bat runs 22.
   Anything past 12 cannot be outrun at all.
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
  the main source of a large mid-game jump — but they are found, never
  bought, and nothing on the first dungeon levels is guaranteed, so a
  character that has not found one has no way to acquire it.
- **A backpack's weight limit matters**: a level-0 wizard can carry very
  little before becoming encumbered, and encumbered characters act
  slower and suffer worse to-hit.

## What this file does not know

- Behaviour of the 68 identities not being played.
- Creatures above level 2, though `src/monst.c` has all
  390 and raising `LEVEL_BAND` in the generator will add them.
- Spell mechanics: casting costs, hunger per spell, and the damage
  numbers a level-0 wizard can actually produce. That is the largest
  gap, and it is the most likely place a real improvement lives —
  a wizard who can actually cast would not need most of rule 1 above.
- Anything about the bot's own code, what the loop is trying to achieve,
  what has already been tried, or how anything has performed. That is
  in the brief and in `experience.md`.

---

Every number above is parsed from the tagged NetHack `NetHack-3.6.6_Released` source
(`src/monst.c`, `src/role.c`, `include/align.h`), not recalled. This file
is generated, and it contains game data only — no results, no
measurements, and no recommendations.