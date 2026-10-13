# Next experiment

## Result

- iteration 1: 0.14320 kept (registered). Increases the mean by 0.00534 (from 0.13786 to 0.14320). Rewrote `get_potential_wand_usages` in `autoascend/combat/fight_heur.py`. Only seed 8 changes (Xp:6 -> Xp:9, 0.0369 -> 0.1170); the other 14 seeds match the parent.

## Proposal

Rewrite the one function `get_potential_wand_usages` in
`autoascend/combat/fight_heur.py`.

The function scores a wand shot by walking the beam/ray with
`simulate_wand_path` and adding points for every monster on the path. A
floating eye on the path is scored like any weak monster. That is wrong when
something is standing next to the wizard: the eye's passive gaze freezes the
wizard the moment it is hit, and any adjacent monster then attacks it while it
cannot act.

Seed 8 shows the loss exactly. The wizard, forced to attack while its
exploration stalls on dungeon level 1, fires its wand of magic missile at a
floating eye, is frozen by the gaze, and is bitten to death by a newt at Xp:6.

The rewrite adds one clause. Before scoring, compute whether any non-eye
monster is within 2 tiles of the wizard. If one is, a floating eye on a wand
path is scored far below every other action, so the bot does not shoot it. If
no non-eye monster is close, the eye keeps its normal score and the bot may
still clear it from a safe distance.

## Why it stopped

The 15 public seeds (`secret="public"`, `evaluation_id="local"`) were played on
the changed tree. The parent batch is not in this note.

## What is the problem

Mean progress is unknown to the bot. The bot is kept only if the next mean is
strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of
15 seeds. A child is kept only when that mean is strictly higher. One change,
naming the one rewritten function, raises the score and must not be reverted.
The judge scores the tree that is exited with. The change above raises the mean
from 0.13786 to 0.14320 and does not lower any seed.
