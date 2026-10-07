# The fifteen games

All fifteen seeds of `wiz-hum-cha-mal` were played to the end. Progress is the
highest milestone each game reached. The mean is 0.114.

| seed | progress | milestone | deepest level | turns | death |
|---|---|---|---|---|---|
| 0 | 0.1170 | Xp:9 | 1 | 50145 | poisoned by an orcish arrow |
| 1 | 0.1791 | Xp:10 | 1 | 46006 | killed by a killer bee |
| 2 | 0.0745 | Xp:8 | 1 | 34154 | killed by a bolt of fire |
| 3 | 0.1791 | Xp:10 | 3 | 57042 | poisoned by an orcish arrow |
| 4 | 0.0185 | Xp:2 | 2 | 2742 | killed by a goblin |
| 5 | 0.1791 | Xp:10 | 1 | 55705 | killed by a giant bat |
| 6 | 0.1791 | Xp:10 | 3 | 73840 | killed by a plains centaur |
| 7 | 0.1170 | Xp:9 | 6 | 34611 | killed by a vampire bat |
| 8 | 0.0369 | Xp:6 | 1 | 9957 | killed by a newt |
| 9 | 0.2548 | Xp:11 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | 0.0242 | Xp:4 | 2 | 6313 | killed by a kitten |
| 11 | 0.0745 | Xp:8 | 4 | 23577 | killed by a pony |
| 12 | 0.0291 | Xp:5 | 2 | 5011 | killed by a kobold lord |
| 13 | 0.1791 | Xp:10 | 5 | 48694 | killed by a dwarf lord |
| 14 | 0.0745 | Xp:8 | 1 | 32018 | killed by a bolt of cold |

## What the games look like

Every game ends in combat. Nothing ever descends far enough for a depth
milestone to matter: the deepest level reached by any seed is 6, worth 0.0354,
and every seed banks a larger experience milestone than that except seeds 4, 8,
10, and 12. The score is therefore the experience banked before death on the
first Doom level.

The wizard grows steadily. Seeds 1, 3, 5, 6, and 13 all stop at experience
level 10, one level short of the 0.2548 cell; seed 9 reaches level 11 and is
the best game. Seeds 0 and 7 stop at level 9. Seeds 2, 11, and 14 stop at
level 8. Four seeds (4, 8, 10, 12) collapse in the first six thousand turns
and never get started.

## How the wizard dies

Six of the fifteen games end to a monster that moves faster than the wizard:
a killer bee (seed 1), a giant bat (5), a plains centaur (6), a vampire bat
(7), a kitten (10), and a pony (11). Four end to a ranged attack or its
poison: two orcish arrows (0, 3), a bolt of fire (2), a bolt of cold (14).
Three end in an ordinary melee trade: a plains centaur, an invisible Mordor
orc (9), and a dwarf lord (13). One ends from paralysis: seed 8. Two of the
remaining early deaths happen while the wizard is fainting from hunger (4 and
12).

Five games end with the wizard at the fainting hunger state (1, 4, 5, 9, 12).
Across all fifteen games the log records thousands of entries at hunger weak
or worse, so food pressure is continuous, not occasional.

## The last turns

The five games that stop at experience level 10 share a shape. The wizard is
in a fair fight, its hit points fall, and it keeps swinging.

Seed 1 ends at 6/81 hit points with a dwarf, a coyote, and a killer bee all
attacking at once in the open. The wizard wrote Elbereth three turns earlier
and both the dwarf and the coyote turned to flee, but the arrows kept coming
and the wizard was fainting. It died of a poisoned sting.

Seed 5 ends at 12/74 with a giant bat. The wizard had just written Elbereth
and the bat turned to flee, but the wizard then spent its remaining turns
putting on a red-eyed shield, putting on a hooded cloak, listing its iron
skull cap and jackboots, opening the terrain display, and dropping the
jackboots. The bat came back and took the last twelve hit points in two turns.

Seed 6 ends at 3/78 against a plains centaur. The wizard opened the terrain
display twice while the centaur landed four blows, threw one dagger, and then
prayed and died mid-prayer.

Seed 13 ends at 18/87 against a dwarf lord. The wizard had been opening the
terrain display and trying to pick up objects from an empty tile, then
"began bashing monsters with your bare hands" and lost the trade in five
turns.

Seed 3 ends at 69/78 against a homunculus and a poisoned crude arrow. The
wizard spent several of those turns picking daggers back off the floor instead
of swinging.

## The four short games

Seed 4 lasts 2742 turns. The wizard prayed at 17/17 hit points and its god
called it arrogant; maximum hit points fell from 17 to 12. It prayed again 404
turns later at 12/12 and was called arrogant again; maximum hit points fell
to 7. It then fainted and a goblin finished it. Seed 12 ends the same way,
fainting into a kobold lord at 5011 turns.

Seed 10 lasts 6313 turns. Its own cat stayed on level 1 while it descended to
level 2, where a little dog and then a kitten attacked it. It wrote Elbereth,
the kitten turned to flee, and then the kitten bit it to death while the
wizard stood on the engraving.

Seed 8 lasts 9957 turns. It reached level 6, then ran out of thrown weapons,
zapped a wand that did nothing, and walked up to a floating eye. The gaze
froze it at 46/46 hit points. Ten turns later it could move again, and for the
next ninety-six turns the log contains nothing but "The newt bites!" while a
newt took it from 46 to 0.

## What the log shows happening between the fights

The wizard opens the terrain display constantly: 65 times in seed 4, 2224
times in seed 9. It tries to pick up objects from tiles that hold nothing:
18 times in seed 4, 1703 times in seed 9. It bumps into walls and doorways:
174 times in seed 2, 158 times in seed 13. It re-reads its own Elbereth
engraving while monsters attack. None of this is a strategy; it is the cost of
the bookkeeping the agent does on every turn.

Prayer is the one clearly punitive event. Three hundred and five prayers were
accepted and eight were rejected. Two rejections cost experience levels and
maximum hit points outright: seed 4 twice (17 to 12 to 7), seed 10 (29 to 22),
seed 11 (60 to 54). The four level drains all come from prayers spaced about
four hundred turns apart, which is the fainting branch of the prayer gate.

## What the bot already does well

It eats, it heals, it engraves, it throws before it swings, it wields a weapon
before it trades blows, and it holds the first Doom level until experience
level 12. Those four gates are what moved the mean from 0.064 to 0.114. The
wizard now reaches experience level 9 or 10 in eleven of fifteen games; the
losses are in the fights themselves, not in the trip to them.
