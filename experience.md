# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The judge evaluation of the parent tree (15 seeds) ends every game with a death.
Mean progress: 0.13785727269465212. Milestones reached: Xp:11 x4, Xp:10 x4,
Xp:8 x3, Xp:6 x1, Xp:5 x1, Xp:4 x1, Xp:2 x1. Ends of the games, as recorded by
the judge:

- Xp:10 killed by a coyote (depth 4)
- Xp:11 killed by a dwarf lord (depth 1)
- Xp:8 killed by a bolt of fire (depth 1)
- Xp:11 killed by a fire ant (depth 1)
- Xp:2 killed by a goblin (depth 2)
- Xp:11 killed by a soldier ant (depth 1)
- Xp:10 killed by a hobbit (depth 3)
- Xp:10 poisoned by a rotted rothe corpse (depth 3)
- Xp:6 killed by a newt (depth 1)
- Xp:11 killed by an invisible Mordor orc (depth 3)
- Xp:4 killed by a kitten (depth 2)
- Xp:8 killed by a pony (depth 4)
- Xp:5 killed by a kobold lord (depth 2)
- Xp:10 killed by a dwarf lord (depth 5)
- Xp:8 killed by a bolt of cold (depth 1)

## What is the problem

Most games die on the first floors (max_depth 1-2 for 9 of 15 seeds). Two
deaths come from a bolt of fire / bolt of cold, and five come from monsters far
stronger than the early levels should hold (dwarf lord x2, fire ant, soldier
ant, invisible Mordor orc). All of these are signature effects of fire traps and
magic traps on the starting floors. Eight of the remaining deaths are ordinary
early monsters (coyote, goblin, hobbit, newt, kitten, pony, kobold lord, rotted
rothe poison) met while low-level and weak. The trap bolts and trap-summoned
monsters end four of the five Xp:11 games - the very games whose progress the
score depends on. Stepping onto a known trap is permitted for 50 turns after the
bot is stuck (the unstuck window), and that is how the wizard walks onto the
fire and magic traps that kill it.

## What might solve it

Do not walk onto known fire traps and known magic traps on the first two floors,
even during the unstuck window that normally treats known traps as walkable.
This avoids the bolts of fire and the trap-summoned monsters, while deep floors
keep the escape hatch unchanged.