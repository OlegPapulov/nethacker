# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## The fifteen games

The parent tree scores a mean of 0.1328 over the fifteen judge seeds (the reference
run `/refs/parent-eval.json`). Progress is the highest milestone a game reached, and
on this character the milestone is almost always an experience level: every game
banks its best level on the first Doom floor and then dies before the next level.
The seeds split into three bands.

- Xp:11 -> 0.2548: seeds 3, 6, 9. The best games. Seed 6 also walks down to Dlvl:6
  (81066 turns), seed 3 and 9 reach only Dlvl:1 and Dlvl:3. All three die in melee
  or to an invisible attacker (spotted jelly / housecat / invisible Mordor orc).
- Xp:10 -> 0.1791: seeds 0, 1, 5, 7, 13. Killed by a giant bat, a killer bee (twice),
  a rotted corpse, and a dwarf lord.
- Xp:8 or below -> 0.0185 to 0.0745: seeds 2, 4, 8, 10, 11, 12, 14. Seeds 4, 10, 12
  die in the first few thousand turns (Xp:2, Xp:4, Xp:5) to a goblin, a kitten and a
  kobold lord; seed 8 dies to a newt at Xp:6; seeds 2 and 14 die to monster wands
  (bolt of fire / bolt of cold); seed 11 dies to a pony at Xp:8.

## What the deaths say

Grouped by cause the fifteen deaths are:

- faster monsters -- giant bat, killer bee x2, housecat, kitten, pony: six games.
  The agent already knows these (`is_monster_faster`) and melees them; the movement
  and Elbereth answers to them are exactly the changes listed as already measured.
- ordinary melee -- goblin, newt, kobold lord, dwarf lord, spotted jelly: five games.
- monster wands -- bolt of fire, bolt of cold: two games.
- invisible attacker -- invisible Mordor orc: one game.
- the wizard's own food -- seed 7, "poisoned by a rotted rothe corpse": one game.

The last one is the only death the agent never even tries to answer. Every other
death is either something the listed tests already cover or something no cheap edit
can see (an invisible monster, a monster's wand). Food poisoning, by contrast, is
written down in plain text on the status line and can be cured with one action.

## Seed 7 in detail

Seed 7 finishes at Xp:10 on Dlvl:3 after 60316 turns and dies "poisoned by a rotted
rothe corpse". That phrasing is NetHack's food-poisoning death: the wizard ate a
corpse that had rotted past the fifty-turn freshness window, went `Sick`, and died on
the poison timer. Nothing in the agent reacts to `Sick`. The `emergency_strategy`
only prays when hit points are low (`hp < 6`) or hunger is `FAINTING`, and food
poisoning kills on a timer while the wizard can still be at high hit points, so the
existing prayer never fires for it. The corpse-refresh at `autoascend/agent.py:1478`
is the mechanism that lets the rotted corpse look fresh, and that refresh is a listed
test (line 69 of `GAME_RULES.md`), so it must be left alone. The cure, not the meal,
is the part that is missing.

## What might solve it

See `experiments.md`.
