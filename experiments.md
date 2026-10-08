# Next experiment

## Proposal

One existing test, not named in GAME_RULES: the melee-engagement gate for molds.

In `combat/movement_priority.py`, `draw_monster_priority_positive` lets the wizard freely engage
a non-ranged-slow mold only when `hitpoints >= 15 or hitpoints == max_hitpoints`. Molds on the
early Doom floors (green mold, yellow mold, and friends) are slow and nearly harmless, so they
are the safest xp source the character has while it farms to level 12. When the wizard is a few
levels into the farm, max hp is low enough that `hp >= 15 or hp == max_hp` is often false in the
12-14 range, so the bot wanders past these free kills instead of grinding them.

Lower the mold gate from 15 to 12: at 12-14 hp the wizard now closes into melee on molds and
banks their xp instead of walking by. The unicorn branch keeps its 15-gate, so only this one
test changes. This directly raises the xp income on the floors the bot lives on, pushing seeds
that die between a level boundary over that boundary. The risk is bounded because molds deal
small damage and the gate still refuses to engage below 12 hp.

## Result

- Not yet judged. Justification: banked milestone = highest xp level reached; grass-farming a
  slow monster cannot reduce milestone monotone-ness unless it shifts the death earlier, which
  a 12-hp gate on a ~1-2 damage monster makes unlikely.

## Last iteration

The previous tree scored 0.094 and was not kept. Do not submit that same diff again.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on
`wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Change
one test that already exists. Do not add a new action. Describe the games in `experience.md`.
Propose one change in this file, in accordance with the game rules. Change the bot from that
proposal. The judge measures that tree.