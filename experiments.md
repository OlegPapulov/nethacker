# Next experiment

## Result

The parent tree scores 0.1328 over the fifteen judge seeds. The fifteen games and
their deaths are in `experience.md`. The one death the agent never answers is seed
7's food poisoning ("poisoned by a rotted rothe corpse"), and that is the death this
edit answers.

## What is the problem

`autoascend/agent.py` never reacts to the NetHack status condition that the game
writes for a bad meal. `Sick` shows on the bottom status line as `FoodPois` (food
poisoning, the rotted-corpse case) or `TermIll` (a monster's terminal illness), and
food poisoning kills on a timer even while the wizard is at full hit points. The only
cure code in the tree is `cure_disease`, and it handles lycanthropy only. The
`emergency_strategy` prayer fires at `hp < 6` or hunger `FAINTING`, so a full-health
wizard with food poisoning sits there and dies on schedule. Seed 7 is exactly that.

The corpse-refresh in `agent.py:1478` is what lets a rotted corpse look fresh; that
refresh is a listed test (`GAME_RULES.md` line 69), so it is left untouched. The
missing piece is the antidote, not the meal.

## What might solve it

Teach `cure_disease` to answer the `Sick` condition, using only resources the wizard
already has and never changing a listed test:

- Add a `Property.sick` that reads the same bottom status line the existing
  `confusion` / `stun` / `hallu` / `blind` properties read, and returns true when it
  contains `FoodPois`, `TermIll`, or `Ill`.
- In `cure_disease`, when the wizard is sick, eat a lizard corpse from the pack if it
  carries one (a lizard corpse cures illness, and it is exempt from the rot check for
  exactly that reason), otherwise pray, but only inside the same `is_safe_to_pray()`
  window the rest of the agent uses so a sickness right after a prayer cannot anger
  the god.

This is additive and self-limiting: when the wizard is not sick it does nothing at
all, so no game that never gets poisoned can change. It is not gated on experience
level, hit points, or hunger, so it also covers a poisoned wizard that the
`hp < 6` prayer would never reach.

It does not touch any listed test: not the prayer numbers (line 59, still `hp < 6`
and the `FAINTING` wait), not the corpse walk or its latch (lines 60, 62), not the
eat distances (line 63), not the melee bonus (line 61), not the wand path or penalty
(line 64), not the doorway bonus (line 65), not the striking wand (line 66), not the
skill choice (line 67), not the Elbereth write (line 68), and not the corpse refresh
(line 69).

## Change

Implemented in `autoascend/character.py` (`Property.sick`) and
`autoascend/agent.py` (`cure_disease`). The judge measures that tree.
