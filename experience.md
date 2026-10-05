# Playthrough

Identity: `wiz-hum-cha-mal` (chaotic human wizard, male)

## The fifteen games

Every seed is a completed episode: the bot never stalls, never quits and never
errors out -- all fifteen end in a genuine NetHack death, read back from the
xlogfile `death=` string. Mean progress **0.1144**.

| seed | progress | milestone | deepest dlevel | turns | death |
|------|----------|-----------|----------------|-------|-------|
| 0  | 0.1170 | Xp:9  | 1 | 50145 | poisoned by an orcish arrow |
| 1  | 0.1791 | Xp:10 | 1 | 46006 | killed by a killer bee |
| 2  | 0.0745 | Xp:8  | 1 | 34154 | killed by a bolt of fire |
| 3  | 0.1791 | Xp:10 | 3 | 57042 | poisoned by an orcish arrow |
| 4  | 0.0185 | Xp:2  | 2 | 2742  | killed by a goblin |
| 5  | 0.1791 | Xp:10 | 1 | 55705 | killed by a giant bat |
| 6  | 0.1791 | Xp:10 | 3 | 73840 | killed by a plains centaur |
| 7  | 0.1170 | Xp:9  | 6 | 34611 | killed by a vampire bat |
| 8  | 0.0369 | Xp:6  | 1 | 9957  | killed by a newt |
| 9  | 0.2548 | Xp:11 | 3 | 69906 | killed by an invisible Mordor orc |
| 10 | 0.0242 | Xp:4  | 2 | 6313  | killed by a kitten |
| 11 | 0.0745 | Xp:8  | 4 | 23577 | killed by a pony |
| 12 | 0.0291 | Xp:5  | 2 | 5011  | killed by a kobold lord |
| 13 | 0.1791 | Xp:10 | 5 | 48694 | killed by a dwarf lord |
| 14 | 0.0745 | Xp:8  | 1 | 32018 | killed by a bolt of cold |

## What the milestone column means

The scorer (`nethackers/arena/progress.py`) is a running **maximum** over the
BALDROG achievement table, and the bot's own `current_strategy()` names the
milestone. Every one of the fifteen games is named by its experience level --
`Xp:8` = 0.0745, `Xp:9` = 0.1170, `Xp:10` = 0.1791, `Xp:11` = 0.2548 -- and in
no seed does a depth milestone ever win. The deepest the bot ever gets is
dlevel 6 and the deepest that ever *scores* is dlevel 5 (0.0265), so the whole
0.114 mean is bought on the Dungeons of Doom.

## Why it stopped

The bot leaves `global_logic.current_strategy()` in the `BE_ON_FIRST_LEVEL`
branch, whose gate is `experience_level >= 12`, and no seed ever gets there:
the best game in the batch stops one point short at `Xp:11`. So the gate is
never reached, the milestone never advances past the first floor, and the bot
spends the entire episode -- 2,742 to 73,840 turns -- clearing the same one or
two Doom floors for experience. That is not a stall: it is forty thousand turns
of deliberate farming.

Every one of those forty thousand turns is fought with a knife.

A human wizard at these levels has three to forty hit points and no ranged
attack, and `fight_heur` gives melee priority 16 whenever the wizard is above 8
hit points, so `fight2` walks the wizard into everything it sees and trades.
That is what the `death=` column records, and it is not a list of monsters that
out-fought a wizard. Three seeds die to a **goblin**, a **kitten** and a **newt**
-- monsters that do one or two damage a hit -- because the wizard was standing
next to them at one or two hit points with no way to heal
(`emergency_strategy` only quaffs a *identified* healing potion, and only below
a third of max hit points; below one fifth it prays, and one fifth of a
five-hit-point wizard is a hit point it never reaches). Five more seeds die to
monsters flagged by the agent's own `is_monster_faster` -- killer bee, giant
bat, vampire bat, kitten, pony -- which the rules name exactly: a faster monster
takes a turn before the wizard takes a turn, so the wizard loses twice the
health race it entered.

Turn count then tracks experience almost perfectly (2,742 turns -> Xp:2;
9,957 -> Xp:6; 23,577 -> Xp:8; 69,906 -> Xp:11). The bot is not losing levels to
bad play in the deep dungeon; it is losing them to dying early on floor one.
Seeds 4, 10, 12 and 8 die within the first 10,000 turns at `Xp:2`, `Xp:4`,
`Xp:5` and `Xp:6`, and those four seeds alone are worth 0.040 of the 0.065 gap
between this run's mean and a mean where every seed reached `Xp:10`.

## What is the problem

The bot has one tool -- walk next to the thing, hit it with a knife, take a hit
back -- on a character whose whole reason for existing is that it does not have
to. `emergency_strategy` carries the only caster code in the tree and it is all
commented out (`should_cast_heal`, `should_cast_extra_heal`, the force bolt
line), so every spell in the game is unreachable. `main()` reads the cast menu
at turn 0, so `character.known_spells` is populated, and nothing ever calls
`cast()`.

Every turn spent inside melee range is a turn in which the wizard's only
defense is hit points it cannot regenerate. Its one safe way to kill is at a
distance, and it has never taken it.

## What might solve it

See `experiments.md`.