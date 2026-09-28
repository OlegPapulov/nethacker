# heuristic monster types lists
ONLY_RANGED_SLOW_MONSTERS = ['floating eye', 'blue jelly', 'brown mold', 'gas spore', 'acid blob']
EXPLODING_MONSTERS = ['yellow light', 'gas spore', 'flaming sphere', 'freezing sphere', 'shocking sphere']
INSECTS = ['giant ant', 'killer bee', 'soldier ant', 'fire ant', 'giant beetle', 'queen bee']
WEAK_MONSTERS = ['lichen', 'newt', 'shrieker', 'grid bug']
WEIRD_MONSTERS = ['leprechaun', 'nymph']


def is_monster_faster(agent, monster):
    _, y, x, mon, _ = monster
    # TOOD: implement properly
    return 'bat' in mon.mname or 'dog' in mon.mname or 'cat' in mon.mname \
           or 'kitten' in mon.mname or 'pony' in mon.mname or 'horse' in mon.mname \
           or 'bee' in mon.mname or 'fox' in mon.mname


# hypothesis: the hitpoint level at which the bot stops trying to win a fight is an
# absolute number (8, or 16 against a "dangerous" monster) that fits a character with a
# dozen hitpoints, not a wizard that carries 50+ by experience level 6. With the same
# constants the wizard walks into a fight already one hit from death, and the trace shows
# it dying in bursts while at full hitpoints because it never disengaged early enough.
# Scale the threshold with the character's own maximum instead.
MIN_HP_FRACTION_FOR_MELEE = 1 / 3
MIN_HP_ABSOLUTE_FOR_MELEE = 8


def imminent_death_on_melee(agent, monster):
    threshold = max(MIN_HP_ABSOLUTE_FOR_MELEE,
                    MIN_HP_FRACTION_FOR_MELEE * agent.blstats.max_hitpoints)
    if is_dangerous_monster(monster):
        threshold = max(16, 2 * threshold)
    return agent.blstats.hitpoints <= threshold


def is_dangerous_monster(monster):
    _, y, x, mon, _ = monster
    is_pet = 'dog' in mon.mname or 'cat' in mon.mname or 'kitten' in mon.mname or 'pony' in mon.mname \
             or 'horse' in mon.mname
    # 'mumak' in mon.mname or 'orc' in mon.mname or 'rothe' in mon.mname \
    # or 'were' in mon.mname or 'unicorn' in mon.mname or 'elf' in mon.mname or 'leocrotta' in mon.mname \
    # or 'mimic' in mon.mname
    return is_pet or mon.mname in INSECTS


def consider_melee_only_ranged_if_hp_full(agent, monster):
    return monster[3].mname in ('brown mold', 'blue jelly') and agent.blstats.hitpoints == agent.blstats.max_hitpoints
