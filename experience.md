# Playthrough

Identity: `wiz-hum-cha-mal` (chaotic male human wizard).

## The games

These are the ends of the fifteen games the parent bot played (`/refs/parent-eval.json`).
Progress is the highest milestone reached; the score is the mean of the fifteen.

| seed | progress | milestone | depth | turns | cause of death |
|-----:|---------:|-----------|------:|------:|----------------|
| 0  | 0.179 | Xp:10 | 2 | 56,851 | killed by a giant bat |
| 1  | 0.179 | Xp:10 | 1 | 46,006 | killed by a killer bee |
| 2  | 0.074 | Xp:8  | 1 | 34,154 | killed by a bolt of fire |
| 3  | 0.255 | Xp:11 | 1 | 69,782 | killed by a spotted jelly |
| 4  | 0.018 | Xp:2  | 2 |  2,742 | killed by a goblin |
| 5  | 0.179 | Xp:10 | 1 | 56,808 | killed by a killer bee |
| 6  | 0.255 | Xp:11 | 6 | 81,066 | killed by a housecat |
| 7  | 0.179 | Xp:10 | 3 | 60,316 | poisoned by a rotted rothe corpse |
| 8  | 0.037 | Xp:6  | 1 |  9,957 | killed by a newt |
| 9  | 0.255 | Xp:11 | 3 | 69,906 | killed by an invisible Mordor orc |
| 10 | 0.024 | Xp:4  | 2 |  6,313 | killed by a kitten |
| 11 | 0.074 | Xp:8  | 4 | 23,577 | killed by a pony |
| 12 | 0.029 | Xp:5  | 2 |  5,011 | killed by a kobold lord |
| 13 | 0.179 | Xp:10 | 5 | 48,694 | killed by a dwarf lord |
| 14 | 0.074 | Xp:8  | 1 | 32,018 | killed by a bolt of cold |

Mean progress: **0.1328**.

## Why it stopped

Every game ends in the same way: the wizard is killed at melee range. The
killers are fast or hard-hitting monsters that close the distance before the
wizard can answer -- a giant bat, two killer bees, a spotted jelly, a housecat,
a kitten, a pony, a dwarf lord, a kobold lord, a goblin. Four games die very
early (0.018, 0.024, 0.029, 0.037 in the first few thousand turns) and eight
never get past experience level 8.

The wizard owns the exact tool this situation calls for -- a ranged attack
spell -- and it is almost never offered. `combat/fight_heur.py:cast_attack_actions`
only proposes force bolt when the wizard is **experience level 10 or higher**
*and* standing on the **first Doom level** (`agent.blstats.depth == 1`). Two
consequences follow directly from the table above:

- The four early games (seeds 4, 8, 10, 12) die at Xp 2-6. They never reach the
  level-10 gate, so the spell is dead code in exactly the games that need it.
- The games that make it to the deep floors (seeds 0, 6, 7, 9, 11, 13) fight
  and die on depths 2-6, where `depth != 1` switches the spell off. The wizard
  walks into melee with a full energy bar it never spends.

The wizard's energy has no other sink in this agent: the only other caster is
the healer, and its healing spells are gated to the healer role. So every turn
the wizard spends full of Pw without casting is a free ranged attack thrown
away while it is being bitten.

## What might solve it

Offer the attack spell from the first level and on every dungeon level, so a
low-level or descending wizard can kill approaching monsters at range instead
of trading blows. See `experiments.md`.
