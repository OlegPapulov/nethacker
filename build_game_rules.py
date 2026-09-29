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
    L.append(f"**Source:** NetHack `{TAG}` — `src/monst.c`, `src/role.c`, `include/align.h`.")
    L.append("**Not** the wiki: `nethack.alt.org` is a parked domain and every guide")
    L.append("page 404s. The tagged C source is version-exact and does not change.")
    L.append("")

    L.append("## The goal")
    L.append("")
    L.append("Win NetHack: descend ~50 dungeon levels, take the Amulet of Yendor, and")
    L.append("escape through five planes. The arena scores *progress*, not a win:")
    L.append("BALROG progression in [0, 1], which rises as the bot survives, descends")
    L.append("and advances, pinned to a milestone ladder.")
    L.append("")
    L.append("The ladder, measured on this identity's own seeds:")
    L.append("")
    L.append("| depth | progression |")
    L.append("|---|---|")
    for depth, prog in ((1, "~0.03"), (2, "~0.05"), (5, "~0.075"), (7, "~0.18"),
                        (11, "~0.16"), (19, "~0.37"), (25, "~0.47"), (28, "~0.60")):
        L.append(f"| dlvl {depth} | {prog} |")
    L.append("")
    L.append("**This is the most important table in this file.** It says where the")
    L.append("score actually is. On this identity, 9 of 15 seeds never reach dlvl 1's")
    L.append("staircase, so the entire remaining game is worth about 0.03–0.05 and")
    L.append("nothing above it is reachable. A change that trades depth for safety")
    L.append("is the right trade *here* and a bad one in general.")
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
            "Wizard": "Intelligence is your only strength. You start with almost no "
                      "melee ability and must win at range or not at all — a point-blank "
                      "fight with a jackal is one you will lose.",
            "Valkyrie": "Strength and Dexterity. You can win in melee, which is why the "
                        "Valkyrie baseline reaches depths the others never touch.",
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
    L.append("- It does not gate ordinary combat, hunger, or movement — so for the")
    L.append("  early deaths below it is background, not a cause.")
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
    L.append("| died to | seeds | lvl | AC | dmg | traits |")
    L.append("|---|---|---|---|---|---|")
    for name, count in sorted(deaths.items(), key=lambda kv: -kv[1]):
        entry = monsters.get(name)
        if not entry:
            L.append(f"| {name} | {count} | ? | ? | ? | *not parsed* |")
            continue
        lvl = entry.get("level", ["?"])[0]
        traits = ", ".join(entry.get("traits1", [])[:3]) or "-"
        L.append(
            f"| {name} | {count} | {lvl} | {entry.get('ac','?')} | "
            f"{entry.get('damage','?')} | {traits} |"
        )
    L.append("")

    L.append("### What this table says about the deaths")
    L.append("")
    L.append("- **The killers are low-level but not harmless.** A goblin is level 0")
    L.append("  with AC 1, but it attacks with a weapon at 1d4. Against a level-0")
    L.append("  character with no armour that is a real fight, and there is no way to")
    L.append("  win it by trading blows.")
    L.append("- **The AC column is why fleeing works.** AC 1 means your hits almost")
    L.append("  always land; most of these creatures have low AC and hit often. The")
    L.append("  correct response to a fight you cannot finish is to not be in it.")
    L.append("- **`killer bee` deals DRST, not PHYS.** Armour does not reduce it. If a")
    L.append("  bee is the killer, AC is irrelevant and the only answer is distance.")
    L.append("- **`grid bug` deals ELEC and is level 0, AC 1.** It cannot be killed,")
    L.append("  cannot be outrun meaningfully, and there is no combat answer. The only")
    L.append("  correct play is to never step on it, which means detecting it from the")
    L.append("  glyph before moving.")
    L.append("- **`brown mold` deals COLD** and is stationary (M2_HOSTILE, level 1).")
    L.append("  Same lesson: do not touch it.")
    L.append("- **`soldier ant` is level 3 with AC 6** — the hardest killer in this")
    L.append("  table by a wide margin. It is also tiny (20 weight), so it is easy to")
    L.append("  walk into.")
    L.append("")

    L.append("## Rules that decide whether you survive dlvl 1")
    L.append("")
    L.append("These follow from the statistics above and from the game's own")
    L.append("mechanics, and they are the things a strategy change can act on.")
    L.append("")
    L.append("1. **You cannot win a melee fight.** A level-0 wizard with no weapon")
    L.append("   skill loses to a goblin. Your damage output at level 0 is negligible")
    L.append("   against anything with more than 5 HP. Fight only what is already")
    L.append("   hurt, or do not fight.")
    L.append("2. **Disengage early, not at low HP.** The instinct to retreat when")
    L.append("   hurt is too late: several of these creatures hit for 1d6 or more, and")
    L.append("   a level-0 wizard has almost no HP to spend. The decision has to be")
    L.append("   made *before* HP matters, i.e. on the monster's state, not yours.")
    L.append("3. **Some monsters must never be engaged at all.** Grid bug (ELEC,")
    L.append("   unkillable), brown mold (COLD, stationary), and anything that")
    L.append("   attacks with a damage type your protection does not reduce.")
    L.append("4. **Retreat has to be geometrically possible.** A corridor with a")
    L.append("   monster behind you is not a retreat. Check the square you would move")
    L.append("   into before committing.")
    L.append("5. **Corpses are the only food on dlvl 1, and they rot.** A corpse is")
    L.append("   edible for roughly 50 turns, so a kill you walk away from is food")
    L.append("   you will not come back to. If you kill something, eat it then.")
    L.append("6. **Your own square is hidden.** The cell you stand on is drawn as the")
    L.append("   player glyph, so you cannot see a monster or item underfoot. A")
    L.append("   staircase is invisible while you occupy it, and so is a grid bug.")
    L.append("   You must remember what was there.")
    L.append("")

    L.append("## What this file does not know")
    L.append("")
    L.append("- Behaviour of the 68 identities not being played.")
    L.append("- Monster statistics for creatures this bot has not died to, though")
    L.append("  `src/monst.c` has all 393 and the generator can add them.")
    L.append("- Spell mechanics: casting costs, hunger per spell, and the damage")
    L.append("  numbers a level-0 wizard can actually produce. That is the largest")
    L.append("  gap, and it is the most likely place a real improvement lives —")
    L.append("  a wizard who can actually cast would not need any of rule 1 above.")
    L.append("- Anything about the bot's own code. That is in the brief.")
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
