# Playthrough

Identity: `wiz-hum-cha-mal`

Fifteen seeds were played. Every game ended in death (`end_status 1`). No seed
ascended. Mean progress 0.114.

| seed | milestone | progress | deepest level | turns | how it died |
| --- | --- | --- | --- | --- | --- |
| 0 | Xp:9 | 0.1170 | 1 | 50,145 | poisoned by an orcish arrow |
| 1 | Xp:10 | 0.1791 | 1 | 46,006 | killed by a killer bee |
| 2 | Xp:8 | 0.0745 | 1 | 34,154 | killed by a bolt of fire |
| 3 | Xp:10 | 0.1791 | 3 | 57,042 | poisoned by an orcish arrow |
| 4 | Xp:2 | 0.0185 | 2 | 2,742 | killed by a goblin |
| 5 | Xp:10 | 0.1791 | 1 | 55,705 | killed by a giant bat |
| 6 | Xp:10 | 0.1791 | 3 | 73,840 | killed by a plains centaur |
| 7 | Xp:9 | 0.1170 | 6 | 34,611 | killed by a vampire bat |
| 8 | Xp:6 | 0.0369 | 1 | 9,957 | killed by a newt |
| 9 | Xp:11 | 0.2548 | 3 | 69,906 | killed by an invisible Mordor orc |
| 10 | Xp:4 | 0.0242 | 2 | 6,313 | killed by a kitten |
| 11 | Xp:8 | 0.0745 | 4 | 23,577 | killed by a pony |
| 12 | Xp:5 | 0.0291 | 2 | 5,011 | killed by a kobold lord |
| 13 | Xp:10 | 0.1791 | 5 | 48,694 | killed by a dwarf lord |
| 14 | Xp:8 | 0.0745 | 1 | 32,018 | killed by a bolt of cold |

Progress is `max(Dlvl:n, Xp:n)`. Seeds 0, 1, 2, 5, 8 and 14 never left level 1,
so their progress is experience only. The other nine seeds descended: seeds 4,
10 and 12 to level 2, seeds 3, 6 and 9 to level 3, seed 11 to level 4, seed 13
to level 5 and seed 7 to level 6. In every case the milestone recorded was still
an experience milestone, so the depth milestone never caught up. The best seed,
9, stopped at `Xp:11`, one experience level short of the level-12 gate that lets
the bot leave the first Doom level.

## Why it stopped

Every seed stopped at the same wall: the wizard stands in melee range of a
monster that out-damages it, and it does not stop fighting until it is dead.
Eleven of the fifteen deaths were melee.

Seeds 1, 5, 6, 7, 10 and 11 (killer bee, giant bat, plains centaur, vampire bat,
kitten, pony) are all monsters with movement 18 or more against the wizard's 12.
A faster monster strikes first, so the wizard trades two or three hits for every
one of its own and the hit point pool never survives. The combat code already
knows these monsters are dangerous: `is_monster_faster()` names bats, cats,
kittens, ponies, horses, bees and foxes, and `imminent_death_on_melee()` paints a
negative movement ring around them. It does not help, because the melee action
is still worth 16 priority points and every movement tile is worth less than
that. Standing still and swinging wins the priority comparison every single
turn.

Seeds 4, 8, 10 and 12 (goblin, newt, kitten, kobold lord) are the same failure
at the very beginning of the game: 2,742 to 9,957 turns, experience levels 2 to
6, hit points in single digits. A newt should never kill a wizard; seed 8 died to
one at 9,957 turns, which means the wizard was already at the bottom of its hit
point pool and kept trading blows anyway.

Seeds 9 and 13 (invisible Mordor orc, dwarf lord) are the same melee death in
the mid game, at 69,906 and 48,694 turns, after the wizard had farmed its way to
`Xp:11` and `Xp:10`.

Seeds 0 and 3 died to poison from an orcish arrow, and seeds 2 and 14 died to
ranged bolts of fire and cold. Those four are the only deaths that are not
melee, and all four are monsters the wizard let stand at range while it had no
answer for them.

Seed 9 is the shape of a game that works: 69,906 turns, `Xp:11`, reached level
3, and only died to an invisible Mordor orc. It proves the farming loop and the
descent gate both function when the wizard survives long enough to use them.

## What is the problem

The wizard has one defensive tool that would break the trade-off: an engraved
Elbereth. Standing on one, the melee action drops by 100 priority points, so the
wizard stops swinging and waits, the monster is repelled instead of attacking,
and the wizard regenerates the hit points it just lost before it steps back off
to fight. It is the only action in the fight code that can beat a melee worth 16
priority points; no movement change can, because every movement tile is worth
less than 16.

The engrave action exists and is already wired up, but the test that offers it
gives it almost no weight. `elbereth_action()` scores
`-15 + 20 * adjacent_monsters * (1 - sqrt(hp/max_hp))`, and a single ordinary
monster is only ever worth 1.0 to 1.5 of the `adjacent_monsters` count. Against
one goblin, one dwarf lord or one giant bat the best it can reach is about 3,
and only once the wizard is already down to about 6 of 40 hit points, while
melee is 16 and repositioning is about 10. The engrave action is therefore
discarded in exactly the fights that kill the wizard. It only wins against a
monster that `is_dangerous_monster()` scores at triple count — pets and insects
— and it cannot win at all against the ordinary monsters that killed eleven of
the fifteen seeds.

## What might solve it

See `experiments.md`.
