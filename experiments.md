# Next experiment

## Proposal

Cast `force bolt` from the first levels, not from experience level 10.

`cast_attack_actions` in `autoascend/combat/fight_heur.py` already builds the
wizard's ranged force-bolt attack — a clear line, a target 2 to 8 squares away,
no pet, no weak monster, the spell known, a failure chance at most 0.15, at
least 10 energy, on the first Doom level — but it was guarded by
`experience_level < 10`. The games that score worst die at experience levels 2,
4, 5 and 6, so that gate never opens for them and the bolt always arrives too
late. Remove that one gate and change nothing else: the energy reserve keeps a
first-level wizard (six energy, below the reserve) from spending its budget, and
from level 2 (fifteen energy) the wizard can hit the monster it would otherwise
have to meet in melee. This is one behavior the listed assumptions do not cover;
no listed test is touched.

The change is measured on the private judge seeds after exit.

## Result

- iteration 1: proposed (not judged). Cast force bolt from the first levels instead of experience level 10. On a local replay of 15 sample seeds the child raised Xp on seeds 1, 6, 9 and 13 and lowered it on seed 2 (a fainting death); the local sum of Xp progress rose from 0.385 to 0.409. Sample seeds are not the private judge seeds.

## Last iteration

The parent tree is the registered 0.114. This edit is built directly on it and
has not been judged yet. The previous tree mentioned below scored 0.064 and is
long gone; do not submit that diff again.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Leave every listed test as it is, including a nearby number in the same function. Do not change a number in an existing test. Add one behavior the listed tests do not already cover. That behavior raises the experience level a game reaches. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
