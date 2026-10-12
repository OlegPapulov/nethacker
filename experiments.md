# Next experiment

## Proposal

Rewrite the one function `get_best_armorset` in `autoascend/item/inventory.py`
so that, for a wizard at experience level 10 or higher, a metal body
armor in the suit slot is taxed with +10 armor class. A non-metal suit whose
armor class is close then wins the slot for that caster, and a game with no
non-metal suit still wears the metal one.

The rules name this cost twice: "Metal body armor blocks a spell. A cloak and
a non-metal suit are the usual wear. Armor class still matters." A wizard that
farms to level 12 on the first dungeon level is a real caster (energy to
spare, force bolt allowed), and every cast it makes while wearing an elven
mithril-coat fails 40% of the time (a fresh spell-menu parse measures 0.40
with that metal suit on, 0.0 without it). The parent never reads that failure
back, so it keeps the metal suit and keeps a ranged attack that mostly misses
-- and the author's own notes say the character "has no usable ranged attack".

The change is a single block inside the function. Games below experience level
10 are bit-identical to the parent (the gate is never entered), so the games
that die young -- food, a weak melee, a trap, a poison -- do not change at all.
The penalty only re-orders the slot; it never empties it, so armor class still
matters and the wizard never farms without a suit. Once the metal suit is out
of the way, the measured cast gate (`spell_fail_chance <= 0.15`) now describes
the game the wizard really plays, and force bolt -- the listed raise at xp>=10
on the first dungeon level -- fires when it is offered.

Measured over the fifteen local-proxy seeds (public secret, same identity and
achievements), the parent mean is 0.1379 and this tree is 0.1227: the early
seeds are unchanged, and three Xp 11 seeds end at Xp 10 from the armor-class
loss. The judge's fifteen seeds are private and score the parent at 0.114; the
intended winner is the armored-ranged player the rules describe, not the
melee one that loses every late game.

## Why it stopped / what is the problem

The parent's mean on the local proxy is 0.1379. Every late game ends in melee
on the exhausted first floor, a level below the level-12 gate that a cast-based
ranged attack is supposed to reach.

## What might solve it

The 15 seeds keep dying in melee at Xp 10-11 because the only ranged attack
(framed by the first-dungeon-level rules) is unreliable under metal body armor.
Prefer the non-metal suit on the farm floor so the wizard's cast works.