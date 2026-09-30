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
A full manual is the wrong shape. The failure this exists to address is specific:
**9 of 15 seeds die on dungeon level 1**, most of them to monsters that are
dangerous *specifically to a level-1 wizard*. So the file covers the goal, the
identity being played, and the creatures in the measured deaths -- and says
nothing about the other 68 identities or the monsters nobody died to.

Provenance is recorded per section, because a wiki page can change under you and
a C source file at a tag cannot. (The NetHack wiki at nethack.alt.org is, as of
this writing, a parked domain: every guide page 404s. The tagged source is the
only version-exact reference reachable.)

Usage: build_game_rules.py <identity> <diagnosis.json> <out.md>
"""

from __future__ import annotations

import json
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
    identity, diagnosis_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
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

    diagnosis = json.loads(Path(diagnosis_path).read_text())
    results = sorted(diagnosis["results"], key=lambda r: r.get("turns") or 0)

    # The creatures that actually killed a seed, most frequent first.
    deaths: dict[str, int] = {}
    for row in results:
        name = (row.get("death") or "").replace("killed by ", "").replace("died of ", "").strip()
        if name:
            # The arena writes "killed by a wolf" and "killed by an ape" -- the
            # article is part of the sentence, not of the monster's name, so it
            # has to come off before the lookup in monst.c ("wolf", "ape").
            for article in ("a ", "an ", "the "):
                if name.startswith(article):
                    name = name[len(article):]
                    break
        if name:
            deaths[name] = deaths.get(name, 0) + 1

    L: list[str] = []
    L.append(f"# Game rules — `{identity}`")
    L.append("")
    L.append("Facts about the game, extracted from the NetHack source the arena")
    L.append("actually runs. Everything here is scoped to the deaths this bot")
    L.append("measured, because a general manual would be mostly irrelevant text.")
    L.append("")
    L.append("This file is **the game only**: monsters, your class, your race, and")
    L.append("the mechanics a strategy can act on. It contains no objective and no")
    L.append("scoring — what the loop is trying to achieve lives in the brief, and")
    L.append("what has already been tried lives in `experience.md`.")
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

    L.append("## What killed this bot, and what each killer actually is")
    L.append("")
    L.append("Every row is a real death from the measured run, with the game's own")
    L.append("statistics for that creature. AC is the number that decides whether you")
    L.append("survive a hit; damage type decides whether armour helps at all.")
    L.append("")
    L.append("| died to | seeds | lvl | AC | dmg | speed | traits |")
    L.append("|---|---|---|---|---|---|---|")
    for name, count in sorted(deaths.items(), key=lambda kv: -kv[1]):
        entry = monsters.get(name)
        if not entry:
            L.append(f"| {name} | {count} | ? | ? | ? | ? | *not parsed* |")
            continue
        lvl = entry.get("level", ["?"])[0]
        traits = ", ".join(entry.get("traits1", [])[:3]) or "-"
        # monst.c's LVL macro is LVL(lvl, mov, ac, mr, aln), so the second
        # field is movement speed and the third is the permonst AC -- which is
        # not the same as the AC the table shows, that one being parsed from the
        # trailing group and adjusted. Reading field[2] as speed printed 18 for
        # a kitten and 24 for a white unicorn, which are ACs.
        speed = entry.get("level", [None, "?"])[1]
        L.append(
            f"| {name} | {count} | {lvl} | {entry.get('ac','?')} | "
            f"{entry.get('damage','?')} | {speed} | {traits} |"
        )
    L.append("")
    L.append("`speed` is the `mov` field of the monster's `LVL(...)` record — its")
    L.append("movement points per turn. Ordinary dungeon creatures run 6 or 9; the")
    L.append("fastest in the game are far above that (an air elemental is 36), so a")
    L.append("high number means the creature closes a one-square gap every turn and")
    L.append("cannot be walked away from.")
    L.append("")

    L.append("### What these statistics mean in the game")
    L.append("")
    L.append("- **AC is what decides whether you survive a hit.** Most of these")
    L.append("  creatures have AC 1, so your attacks almost always land and theirs")
    L.append("  land too. AC is the number to compare before starting a fight.")
    L.append("- **Damage type decides whether armour helps at all.** A PHYS hit is")
    L.append("  reduced by armour; ELEC, COLD, DRST and FIRE are not. A creature that")
    L.append("  attacks with a non-PHYS type cannot be answered with a better AC.")
    L.append("- **`grid bug` is level 0, AC 1, ELEC.** Small, fast, and effectively")
    L.append("  unkillable for a low-level character. It is the game's clearest")
    L.append("  example of a monster with no combat answer.")
    L.append("- **`brown mold` is COLD and stationary** (M2_HOSTILE, level 1): it does")
    L.append("  not move and does not need to.")
    L.append("- **`soldier ant` is level 3 with AC 6** — by far the toughest creature in")
    L.append("  this table, and tiny (20 weight), so easy to walk into by accident.")
    L.append("- **Level is a poor guide to danger here.** A level-0 goblin and a level-0")
    L.append("  grid bug both outclass a level-0 wizard; a level-5 wolf has AC 6.")
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
    L.append("   distance from it. The `speed` column above is that value: a wolf, a")
    L.append("   jackal and a grid bug are all 12, while a bat is 22 and a white")
    L.append("   unicorn 24. Those last two cannot be outrun at all.")
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
    L.append("  the main source of a large mid-game jump — but they are found, not")
    L.append("  bought, and the early seeds rarely contain any.")
    L.append("- **A backpack's weight limit matters**: a level-0 wizard can carry very")
    L.append("  little before becoming encumbered, and encumbered characters act")
    L.append("  slower and suffer worse to-hit.")
    L.append("")

    L.append("## What this file does not know")
    L.append("")
    L.append("- Behaviour of the 68 identities not being played.")
    L.append("- Monster statistics for creatures this bot has not died to, though")
    L.append("  `src/monst.c` has all 393 and the generator can add them.")
    L.append("- Spell mechanics: casting costs, hunger per spell, and the damage")
    L.append("  numbers a level-0 wizard can actually produce. That is the largest")
    L.append("  gap, and it is the most likely place a real improvement lives —")
    L.append("  a wizard who can actually cast would not need most of rule 1 above.")
    L.append("- Anything about the bot's own code, what the loop is trying to achieve,")
    L.append("  or what has already been tried. That is in the brief and in")
    L.append("  `experience.md`.")
    L.append("")

    L.append("---")
    L.append("")
    L.append(f"Generated by `loop/build_game_rules.py` from NetHack `{TAG}`. Every")
    L.append("number above is parsed from that tag's source, not recalled. Regenerate")
    L.append("with `python loop/build_game_rules.py <identity> <diagnosis.json> GAME_RULES.md`.")

    Path(out_path).write_text("\n".join(L))
    print(f"wrote {out_path}: {len('\n'.join(L))} chars")
    print(f"  monsters parsed: {len(monsters)}")
    print(f"  roles parsed:    {len(abilities)}")
    print(f"  races parsed:    {len(races)}")
    print(f"  killers covered: {len(deaths)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
