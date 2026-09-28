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


# hypothesis: how eager the bot is to trade blows is decided by absolute hitpoint
# counts (8, and 16 for a "dangerous" monster) that were tuned for a character with a
# dozen hitpoints. A wizard has 50 by experience level 6, so with the same constants it
# starts a fight with a sliver of health and gets killed by the first monster that
# reaches it. Express both thresholds as a fraction of the current maximum.
MIN_HP_FRACTION_FOR_MELEE = 1 / 3
MIN_HP_ABSOLUTE_FOR_MELEE = 8


def hp_threshold_for_melee(agent, monster):
    """ Hitpoints below which starting a fight with this monster is not worth it """
    threshold = max(MIN_HP_ABSOLUTE_FOR_MELEE,
                    MIN_HP_FRACTION_FOR_MELEE * agent.blstats.max_hitpoints)
    if is_dangerous_monster(monster):
        threshold = max(16, 2 * threshold)
    return threshold


def imminent_death_on_melee(agent, monster):
    return agent.blstats.hitpoints <= hp_threshold_for_melee(agent, monster)


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
