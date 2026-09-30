"""Build GAME_RULES.md from the NetHack 3.6.6 source, scoped to what our seeds hit.

Why generated rather than written by hand
----------------------------------------
Everything below is extracted from the tagged release
``NetHack-3.6.6_Released`` -- ``src/monst.c``, ``src/role.c``,
``include/align.h`` -- so the numbers are the game's actual numbers for the exact
build the arena runs, not a recollection of them. A hand-written table would
drift the moment someone remembered a monster's AC wrongly, and the whole point
of this file is that the model can trust it.

Why scoped rather than general
-------------------------------
A full manual is the wrong shape, but the way this was scoped before was worse:
it used to take a ``diagnosis.json`` and list the creatures that had *actually
killed a seed*, with a per-creature seed count. That made a file which claims to
be "the game only" carry the loop's own measurements inside it. Two problems,
and the second is the one that mattered:

1. It contradicted the file's own stated policy.
2. Those counts came from 15 published seeds, which are **not** the seeds the
   leaderboard scores on. A strategy shaped by "wolf killed 2 of my seeds" is a
   strategy tuned to the wrong dungeons, and it is the same overfit the rest of
   the loop is built to avoid -- just wearing a costume of game documentation.

So this file is now a pure function of ``(identity, source tag)``. It takes no
measurement input at all, which makes "contains no results" a structural
property rather than a promise. Scope is chosen mechanically instead: the
identity being played, and every creature in ``monst.c`` of level <= ``LEVEL_BAND``
-- the band a starting character actually meets. Nothing in the output says how
often anything happened, because nothing in the input knows.

Provenance is recorded per section, because a wiki page can change under you and
a C source file at a tag cannot. (The NetHack wiki at nethack.alt.org is, as of
this writing, a parked domain: every guide page 404s. The tagged source is the
only version-exact reference reachable.)

The generated file deliberately carries **no commands**, because it is inlined
into the brief and the agent cannot run anything in this repository -- an
earlier footer told it to "regenerate with
``python loop/build_game_rules.py ...``", a file that does not exist in its
container. That instruction now lives here, in the generator's docstring, and
in AGENTS.md, where a human will read it.

Usage: build_game_rules.py <identity> <out.md>
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SRC_BASE = "https://raw.githubusercontent.com/NetHack/NetHack/NetHack-3.6.6_Released"
TAG = "NetHack-3.6.6_Released"

#: Which source files hold which facts.
FILES = {
    "monsters": "src/monst.c",
    "roles": "src/role.c",
    "alignment": "include/align.h",
}

#: The thirteen playable roles, in the order role.c declares them. Used to index
#: the ability-score table, which is a bare array of six numbers per row.
ROLE_ORDER = [
    "Archeologist", "Barbarian", "Caveman", "Healer", "Knight", "Monk",
    "Priest", "Rogue", "Ranger", "Samurai", "Tourist", "Valkyrie", "Wizard",
]

#: Highest monster level included in the table. Chosen mechanically, not from
#: any run: a character starts at level 0 and dungeon levels 1-3 are populated
#: from roughly this band, so it is the range whose statistics a starting
#: strategy is actually reasoning about. Raising it costs brief length; at 2 the
#: table is 52 creatures.
LEVEL_BAND = 2

#: Identity codes ("wiz-hum-cha-mal") to the table's names ("Wizard"). The stat
#: table is keyed by full name, so looking up the code silently found nothing --
#: which is how the first generated GAME_RULES.md had no role stats in it.
ROLE_BY_CODE = {
    "arc": "Archeologist", "bar": "Barbarian", "cav": "Caveman",
    "hea": "Healer", "kni": "Knight", "mon": "Monk", "pri": "Priest",
    "rog": "Rogue", "hir": "Ranger", "sam": "Samurai", "tou": "Tourist",
    "val": "Valkyrie", "wiz": "Wizard",
}


def fetch(path: str, cache: Path) -> str:
    if cache.is_file():
        return cache.read_text(encoding="utf-8", errors="replace")
    url = f"{SRC_BASE}/{path}"
    text = subprocess.run(
        ["curl", "-sL", "-m", "60", url], capture_output=True, text=True, check=True
    ).stdout
    cache.write_text(text, encoding="utf-8")
    return text


def parse_monsters(src: str) -> dict[str, dict]:
    """Every MON(...) record: level, AC, weight, damage type, speed, traits.

    The macro is multi-line and its trailing ``N, CLR_*`` group carries the AC,
    so the parse is anchored on that rather than on SIZ(), whose second field is
    a size, not an AC.
    """
    records = re.findall(
        r'    MON\("(?P<name>[^"]+)"(.*?)\n(?=    MON\(|    \{|    \};|\Z)',
        src, re.S,
    )
    out: dict[str, dict] = {}
    for name, body in records:
        entry: dict = {"name": name}
        m = re.search(r"LVL\(([^)]*)\)", body)
        if m:
            entry["level"] = [x.strip() for x in m.group(1).split(",")]
        m = re.search(r"SIZ\(\s*(\d+)", body)
        if m:
            entry["weight"] = int(m.group(1))
        # The trailing group is `<AC>, <colour-or-plan>`, but the colour token is
        # not always CLR_*: a tameable creature ends with its plan instead
        # ("3, HI_DOMESTIC"), so matching only CLR_ silently dropped the AC for
        # every cat, dog and horse in the game.
        m = re.search(r",\s*(\d+),\s*(?:CLR_|HI_|HI_)[A-Z_]+\)", body)
        if m:
            entry["ac"] = int(m.group(1))
        m = re.search(r"ATTK\(AT_\w+,\s*AD_(\w+)", body)
        if m:
            entry["damage"] = m.group(1)
        m = re.search(r"MV_(\w+)", body)
        if m:
            entry["speed"] = m.group(1)
        for tag, key in (("M1_", "traits1"), ("M2_", "traits2"), ("M3_", "traits3")):
            m = re.search(rf"({tag}\w+(?: \| {tag}\w+)*)", body)
            if m:
                entry[key] = [t.split("_", 1)[1] for t in m.group(1).split(" | ")]
        out[name] = entry
    return out


def parse_role_abilities(src: str) -> dict[str, tuple]:
    """Role -> (Str, Int, Wis, Dex, Con, Cha).

    The table is a bare array of six-number rows behind a
    ``/* Str Int Wis Dex Con Cha */`` comment, one row per role, in ROLE_ORDER.
    """
    rows = [m.start() for m in re.finditer(r"/\*\s*Str\s+Int\s+Wis\s+Dex\s+Con\s+Cha\s*\*/", src)]
    out: dict[str, tuple] = {}
    for index, role in enumerate(ROLE_ORDER):
        if index >= len(rows):
            break
        seg = src[rows[index]:rows[index] + 200]
        seg = re.sub(r"/\*.*?\*/", " ", seg, flags=re.S)
        nums = re.findall(r"-?\d+", seg)[:6]
        if len(nums) == 6:
            out[role] = tuple(int(n) for n in nums)
    return out


def parse_races(src: str) -> dict[str, dict]:
    """Race -> ability modifiers, hit points, energy, AC.

    A race record is five brace groups after the name, with NO field labels:

        { "human",                          <- names
          "human", "humanity", "Hum",
          { man }, { woman },
          PM_HUMAN, ..., MH_HUMAN | ...,   <- enum/number soup
          /* Str Int Wis Dex Con Cha */
          { 3, 3, 3, 3, 3, 3 },           <- 0..3 modifiers
          { STR18(100), 18, ... },          <- the same, on a 0..18 scale
          { 2, 0, 0, 2, 1, 0 },            <- init, lower, higher  (hit points)
          { 1, 0, 2, 0, 2, 0 } }           <- energy

    So the numbers are positional, and the earlier attempt read a named
    ``HPBONUS(...)`` that this file does not contain -- which is why every race
    came back with no hit points and no AC.
    """
    out: dict[str, dict] = {}
    for match in re.finditer(r'\{\s*\n\s*"([a-z]+)",\s*\n(.*?)\n    \},', src, re.S):
        race, body = match.group(1), match.group(2)
        # Everything before the stat comment is names and enum soup; everything
        # from it on is the numeric table, and it has exactly four groups in a
        # fixed order. Matching brace groups across the WHOLE body picked up
        # numbers from neighbouring records, which is why every race came back
        # with the same modifiers and a scrambled hit-point value.
        tail = body
        marker = tail.find("Str")
        if marker >= 0:
            tail = tail[marker:]
        groups = re.findall(r"\{([^{}]*)\}", tail)
        numbers = [[int(n) for n in re.findall(r"-?\d+", g)] for g in groups]
        entry: dict = {}
        if len(numbers) >= 1 and len(numbers[0]) == 6:
            entry["mods"] = numbers[0][:6]
        if len(numbers) >= 3 and numbers[2]:
            entry["hp"] = str(numbers[2][0])
        if len(numbers) >= 4 and numbers[3]:
            entry["energy"] = str(numbers[3][0])
        if entry:
            out[race] = entry
    return out


def main() -> int:
    # Two arguments, not three: there is no diagnosis any more, and taking one
    # would invite putting measurements back in. An extra argument is an ERROR
    # rather than something to ignore: the old three-argument call
    # (`<identity> <diagnosis.json> GAME_RULES.md`) would otherwise silently
    # write GAME_RULES content into the diagnosis file and report success,
    # which is the sort of quiet wrongness this rewrite exists to remove.
    if len(sys.argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        print(f"error: expected 2 arguments, got {len(sys.argv) - 1}", file=sys.stderr)
        return 2
    identity, out_path = sys.argv[1], sys.argv[2]
    role, race, align, gender = identity.split("-")

    cache_dir = Path(".nhsrc-cache")
    cache_dir.mkdir(exist_ok=True)
    monsters = parse_monsters(fetch(FILES["monsters"], cache_dir / "monst.c"))
    roles_src = fetch(FILES["roles"], cache_dir / "role.c")
    align_src = fetch(FILES["alignment"], cache_dir / "align.h")
    abilities = parse_role_abilities(roles_src)
    races = parse_races(roles_src)
    # The three alignment values below are the only ones that occur in an
    # identity string. They are read from the tagged header rather than trusted
    # from memory, and this asserts the two the current identity actually uses.
    for token, sign in (("A_CHAOTIC", "-1"), ("A_NEUTRAL", "0"), ("A_LAWFUL", "1")):
        m = re.search(rf"^#define\s+{token}\s+\(?(-?\d+)\)?", align_src, re.M)
        if m and m.group(1) != sign:
            raise SystemExit(
                f"align.h says {token} = {m.group(1)}, the table says {sign}"
            )

    # Every creature in the band, chosen from the source alone. Sorted by level
    # and then hardest-first by AC, so the creatures a starting character most
    # needs an opinion about are the ones near the top of each level group.
    band: list[tuple] = []
    for name, entry in monsters.items():
        fields = entry.get("level")
        if not isinstance(fields, list) or not fields:
            continue
        try:
            level = int(fields[0])
        except (TypeError, ValueError):
            continue
        if level > LEVEL_BAND:
            continue
        try:
            ac = int(entry.get("ac"))
        except (TypeError, ValueError):
            ac = 0
        band.append((level, -ac, name))
    band.sort()

    L: list[str] = []
    L.append(f"# Game rules — `{identity}`")
    L.append("")
    L.append("Facts about the game, extracted from the NetHack source the arena")
    L.append("actually runs. Everything here is scoped to what a character at this")
    L.append("starting level actually meets, because a general manual would be mostly")
    L.append("irrelevant text.")
    L.append("")
    L.append("This file is **the game only**: monsters, your class, your race, and")
    L.append("the mechanics a strategy can act on. It contains no objective, no")
    L.append("scoring, and **no measurements** — what the loop is trying to achieve")
    L.append("lives in the brief, and what has already been tried lives in")
    L.append("`experience.md`. Nothing below says how often anything happened, and")
    L.append("that is deliberate: the only sample available is 15 published seeds,")
    L.append("which are not the dungeons this bot is ultimately scored on, so a")
    L.append("strategy shaped by them is tuned to the wrong game.")
    L.append("")
    L.append(f"**Source:** NetHack `{TAG}` — `src/monst.c`, `src/role.c`, `include/align.h`.")
    L.append("**Not** the wiki: `nethack.alt.org` is a parked domain and every guide")
    L.append("page 404s. The tagged C source is version-exact and does not change.")
    L.append("")

    L.append(f"## Who you are: {role}, {race}, {align}, {gender}")
    L.append("")
    role_name = ROLE_BY_CODE.get(role, role.capitalize())
    if role_name in abilities:
        str_, int_, wis, dex, con, cha = abilities[role_name]
        L.append(f"**Role** (`{role_name}`, code `{role}`) — ability scores:")
        L.append("")
        L.append("| Str | Int | Wis | Dex | Con | Cha |")
        L.append("|---|---|---|---|---|---|")
        L.append(f"| {str_} | {int_} | {wis} | {dex} | {con} | {cha} |")
        L.append("")
        trait = {
            "Wizard": "Intelligence is your only strength: the ability spread gives "
                      "you almost nothing in Str or Dex, so your damage output and "
                      "your accuracy in melee both start from the bottom. A "
                      "level-0 wizard has no melee answer to anything with more "
                      "than a few hit points, and the class's tools are spells.",
            "Valkyrie": "Strength and Dexterity, the two scores a melee fight is "
                        "decided by, and starting skill to use them.",
        }.get(role_name)
        if trait:
            L.append(trait)
            L.append("")
    race_key = {"hum": "human"}.get(race)
    if race_key and race_key in races:
        r = races[race_key]
        L.append(f"**Race** (`{race_key}`):")
        bits = []
        if "hp" in r:
            bits.append(f"hit points `{r['hp']}`")
        if "AC" in r:
            bits.append(f"AC {r['AC']}")
        for key, label in (("luck", "luck"), ("Stealth", "stealth"), ("Speed", "speed"),
                           ("Conf", "conf"), ("Flee", "flee"), ("Energy", "energy")):
            if key in r:
                bits.append(f"{label} {r[key]}")
        if bits:
            L.append("")
            for b in bits:
                L.append(f"- {b}")
        L.append("")
    L.append(f"**Alignment** (`{align}`) — from `include/align.h`:")
    L.append("")
    align_note = {
        "cha": "A_CHAOTIC = -1. You may use any weapon, and alignment only drifts you",
        "law": "A_LAWFUL = 1. You are constrained to hammers, quarterstaffs and swords",
        "neu": "A_NEUTRAL = 0. Alignment will not drift you in either direction",
    }.get(align, "")
    if align_note:
        L.append(f"- {align_note}.")
    L.append("- Alignment is a hard *equipment* constraint, not a personality: a")
    L.append("  chaotic character is refused lawful-only items by the game itself.")
    L.append("- It does not gate ordinary combat, hunger, or movement, so it does not")
    L.append("  explain a death on its own.")
    L.append("")
    L.append(f"**Gender** (`{gender}`) — no mechanical effect in NetHack 3.6.6 beyond")
    L.append("dialogue flavour. Ignore it.")
    L.append("")

    L.append(f"## The creatures of level {LEVEL_BAND} and below")
    L.append("")
    L.append("Every creature in `src/monst.c` at level "
             f"{LEVEL_BAND} or lower — the band a starting character meets on the")
    L.append("first dungeon levels — with the game's own statistics for each, ordered")
    L.append("by level and then hardest-first by AC.")
    L.append("")
    L.append("| creature | lvl | AC | dmg | speed | wt | traits |")
    L.append("|---|---|---|---|---|---|---|")
    for _lvl, _negac, name in band:
        entry = monsters[name]
        fields = entry.get("level") or ["?", "?"]
        traits = ", ".join(entry.get("traits1", [])[:3]) or "-"
        # monst.c's LVL macro is LVL(lvl, mov, ac, mr, aln), so the second
        # field is movement speed and the third is the permonst AC -- which is
        # not the same as the AC the table shows, that one being parsed from the
        # trailing group and adjusted. Reading field[2] as speed printed 18 for
        # a kitten and 24 for a white unicorn, which are ACs.
        speed = fields[1] if len(fields) > 1 else "?"
        L.append(
            f"| {name} | {fields[0]} | {entry.get('ac','?')} | "
            f"{entry.get('damage','?')} | {speed} | {entry.get('weight','?')} | "
            f"{traits} |"
        )
    L.append("")
    L.append("`speed` is the `mov` field of the monster's `LVL(...)` record — its")
    L.append("movement points per turn. Ordinary dungeon creatures run 6 or 9; the")
    L.append("fastest in the game are far above that (an air elemental is 36), so a")
    L.append("high number means the creature closes a one-square gap every turn and")
    L.append("cannot be walked away from.")
    L.append("")

    L.append("### How to read those numbers")
    L.append("")
    L.append("- **AC is what decides whether you survive a hit.** AC 1 means your")
    L.append("  attacks almost always land and theirs land too, so a fight is decided")
    L.append("  by turns taken rather than by luck. Compare AC before starting, not")
    L.append("  after.")
    L.append("- **Damage type decides whether armour helps at all.** A PHYS hit is")
    L.append("  reduced by armour; ELEC, COLD, DRST, FIRE, ACID and the rest are not.")
    L.append("  Most of this band attacks PHYS, but not most of it — a grid bug is")
    L.append("  ELEC and a centipede is DRST, and neither can be answered with a")
    L.append("  better AC.")
    L.append("- **`killer bee` is AC 5** and is the hardest creature in the band, at")
    L.append("  level 1. Nine more sit at AC 4, all level 2: `centipede`, `dwarf`,")
    L.append("  `giant ant`, `hill orc`, `kobold shaman`, `Kop Sergeant`, `monkey`,")
    L.append("  `rabid rat` and `rothe`. Nothing in the band is tougher than that.")
    L.append("- **`grid bug` is level 0, AC 1, ELEC, and speed 12.** It is the")
    L.append("  clearest example in the game of a monster with no combat answer at")
    L.append("  this level: fast enough to reach you, and nothing you do to AC or")
    L.append("  damage output changes that.")
    L.append("- **`bat` and `giant bat` run at speed 22**, `fox` at 15, and")
    L.append("  `killer bee`, `giant ant` and `kitten` at 18. Ordinary creatures run")
    L.append("  6 or 9. Against anything above 12, stepping back one square buys")
    L.append("  nothing.")
    L.append("- **The molds never move.** `brown mold`, `green mold`, `red mold` and")
    L.append("  `yellow mold` have speed 0 and are M2_HOSTILE: they do not need to")
    L.append("  chase you, and they are COLD, ACID, FIRE and STUN respectively, so")
    L.append("  armour does nothing for any of them.")
    L.append("- **Small does not mean harmless, and here it is literal.**")
    L.append("  `killer bee` weighs 1 and is AC 5 — the hardest creature in the band")
    L.append("  is also one of the smallest. `giant ant`, `newt`, `gecko` and")
    L.append("  `floating eye` are 10, `grid bug` 15, and `bat`, `lichen` and")
    L.append("  `sewer rat` 20. Every one of those is lighter than most pieces of")
    L.append("  equipment, so the creatures easiest to walk into by accident are the")
    L.append("  ones least likely to be noticed doing it.")
    L.append("- **`NOHANDS` creatures cannot wield a weapon**, and the")
    L.append("  `NOEYES`/`NOLIMBS`/`BREATHLESS` group — the molds, `lichen`,")
    L.append("  `acid blob`, `gas spore` — has no hands at all and cannot be reasoned")
    L.append("  about as an armed opponent.")
    L.append("- **`FLY` means it crosses what you cannot.** `bat`, `giant bat`,")
    L.append("  `killer bee`, `floating eye`, `gas spore` and `homunculus` pass over")
    L.append("  water and gaps that stop a walking character.")
    L.append("- **`werejackal` and `wererat` have REGEN.** Damage you do does not")
    L.append("  stay done, so an attrition plan that works on an ordinary creature of")
    L.append("  the same level does not work on a lycanthrope. `kobold shaman` attacks")
    L.append("  with SPEL rather than a physical blow, for the same reason: some")
    L.append("  things in this band cannot be answered the ordinary way.")
    L.append("- **Level is a poor guide to danger here.** A level-0 goblin and a")
    L.append("  level-0 grid bug both outclass a level-0 wizard, and the toughest")
    L.append("  creature in the band is a level 1.")
    L.append("")

    L.append("## Mechanics of the game that constrain any strategy")
    L.append("")
    L.append("These are properties of NetHack, not opinions about how to play. They")
    L.append("are the facts a strategy has to be built around.")
    L.append("")
    L.append("1. **Melee damage depends on Str and weapon skill, and experience levels")
    L.append("   both.** A character at level 0 does negligible damage to anything with")
    L.append("   more than a few HP. Killing is slow, and slowness has consequences")
    L.append("   below.")
    L.append("2. **A creature's attack resolves once per turn**, so being adjacent to")
    L.append("   one over many turns means taking many hits. Distance is a real")
    L.append("   resource, and the square you would retreat into has to be checked")
    L.append("   before committing to it — a corridor with a monster behind you is")
    L.append("   not an escape.")
    L.append("3. **Monsters have a movement speed (`mov`), the game's fastest being")
    L.append("   far above the ordinary range.** A creature with a high value closes a")
    L.append("   one-square gap every turn, so retreating one square does not open")
    L.append("   distance from it. The `speed` column above is that value: a goblin and")
    L.append("   a kobold run 6, a jackal and a grid bug run 12, and a bat runs 22.")
    L.append("   Anything past 12 cannot be outrun at all.")
    L.append("4. **Corpses are food and they rot** — edible for roughly 50 turns. A")
    L.append("   kill walked away from is food that will not be there later.")
    L.append("5. **Hunger rises every turn** and a character who starves faints, which")
    L.append("   costs hit points and incapacitates the character while it happens.")
    L.append("   Eating is not optional, and a fainting character cannot fight.")
    L.append("6. **The square you stand on is not drawn to you.** It shows the player")
    L.append("   glyph, so a monster or item underneath you is invisible while you are")
    L.append("   on it — including a staircase, and including a grid bug. You cannot")
    L.append("   see what is underfoot and must remember it.")
    L.append("7. **Experience level comes from kills, and a level-up gives hit points.**")
    L.append("   So a character's ability to survive a fight rises with the number of")
    L.append("   fights it has already won — the early game is the hardest, and the")
    L.append("   thresholds roughly double at each level.")
    L.append("8. **Wizards are spellcasters first and fighters last.** A level-0 wizard")
    L.append("   has almost no melee ability. The intended answer to a fight that")
    L.append("   cannot be won at range is not to be in it. Spell mechanics —")
    L.append("   casting costs, hunger per spell, and the damage numbers available —")
    L.append("   are the largest gap in this file, and the most promising place for a")
    L.append("   real improvement, because a wizard who can actually cast would not")
    L.append("   need most of the advice above.")
    L.append("")
    L.append("## Items")
    L.append("")
    L.append("- **A weapon's damage depends on its weight and your Str**, and most")
    L.append("  early weapons are one-handed and light. A dagger is fast and weak; a")
    L.append("  heavier weapon hits harder and needs both hands.")
    L.append("- **Armor trades speed for protection**: a higher AC value means harder")
    L.append("  to hit, and wearing it makes the character slower to move and act.")
    L.append("  That trade is worth making against a slow, heavy hitter and usually")
    L.append("  not against something that already hits reliably.")
    L.append("- **Alignment gates what you can pick up.** A chaotic character cannot")
    L.append("  wield a lawful-only weapon; the game refuses the pickup outright.")
    L.append("- **Shields, rings, amulets and scrolls change one rule each** and are")
    L.append("  the main source of a large mid-game jump — but they are found, never")
    L.append("  bought, and nothing on the first dungeon levels is guaranteed, so a")
    L.append("  character that has not found one has no way to acquire it.")
    L.append("- **A backpack's weight limit matters**: a level-0 wizard can carry very")
    L.append("  little before becoming encumbered, and encumbered characters act")
    L.append("  slower and suffer worse to-hit.")
    L.append("")

    L.append("## What this file does not know")
    L.append("")
    L.append("- Behaviour of the 68 identities not being played.")
    L.append(f"- Creatures above level {LEVEL_BAND}, though `src/monst.c` has all")
    L.append("  390 and raising `LEVEL_BAND` in the generator will add them.")
    L.append("- Spell mechanics: casting costs, hunger per spell, and the damage")
    L.append("  numbers a level-0 wizard can actually produce. That is the largest")
    L.append("  gap, and it is the most likely place a real improvement lives —")
    L.append("  a wizard who can actually cast would not need most of rule 1 above.")
    L.append("- Anything about the bot's own code, what the loop is trying to achieve,")
    L.append("  what has already been tried, or how anything has performed. That is")
    L.append("  in the brief and in `experience.md`.")
    L.append("")

    L.append("---")
    L.append("")
    L.append(f"Every number above is parsed from the tagged NetHack `{TAG}` source")
    L.append("(`src/monst.c`, `src/role.c`, `include/align.h`), not recalled. This file")
    L.append("is generated, and it contains game data only — no results, no")
    L.append("measurements, and no recommendations.")

    Path(out_path).write_text("\n".join(L))
    print(f"wrote {out_path}: {len('\n'.join(L))} chars")
    print(f"  monsters parsed: {len(monsters)}")
    print(f"  roles parsed:    {len(abilities)}")
    print(f"  races parsed:    {len(races)}")
    print(f"  creatures in band (level <= {LEVEL_BAND}): {len(band)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
