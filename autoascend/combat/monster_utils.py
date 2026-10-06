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


def imminent_death_on_melee(agent, monster):
    if is_dangerous_monster(monster):
        return agent.blstats.hitpoints <= 16
    return agent.blstats.hitpoints <= 8


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


def is_out_trading_us(agent, monster):
    """ Whether a straight melee exchange with this monster would cost us more
    hit points than we can afford to lose.

    A hero's health pool is the budget for a fight.  Putting a monster down in
    melee takes on the order of `difficulty` rounds (its hit points scale with
    that rating), and each round it deals on the order of `difficulty` damage,
    so rating `d` costs roughly `d * d` hit points to exchange blows with.  A
    monster that moves faster than we do lands about twice as many hits during
    that exchange.  When the expected cost exceeds the hit points we actually
    have, we cannot win the trade and must not walk into it -- especially with
    a small pool of hit points.
    """
    _, _, _, mon, _ = monster

    if mon.mname in WEAK_MONSTERS or mon.mname in ONLY_RANGED_SLOW_MONSTERS:
        # These are free to fight: the weak ones barely scratch us and the slow
        # ranged ones cannot hit us in melee.  Keep the existing engage logic.
        return False

    difficulty = getattr(mon, 'difficulty', None)
    if difficulty is None:
        # An unresolved monster (invisible or unknown glyph).  We cannot plan
        # the exchange, so assume the worst rather than charge into it.
        return True

    expected_cost = 2 * difficulty * difficulty
    if is_monster_faster(agent, monster):
        # it acts before we do and again before we do, so roughly twice the hits
        expected_cost *= 2
    return expected_cost > agent.blstats.hitpoints
