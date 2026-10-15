# Next experiment

## Result

- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Submitted the launcher edit again. The 15 seeds match the parent.

## Why it stopped

The current mean is 0.114 on identity `wiz-hum-cha-mal`. The bot farms on dungeon level 1 until experience level 12 (raising score) but dies before reaching significantly higher milestones on many seeds. Survival on early floors is the limiting factor.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Quaffing identified speed potions in emergencies gives the wizard FAST status, improving movement and combat speed. This helps escape danger and fight more efficiently on early floors without violating any listed actions. The change is a rewrite of the `emergency_strategy` function in `autoascend/agent.py` to quaff unambiguous speed potions when in combat or facing imminent threat.

Change: rewrite `autoascend/agent.py::emergency_strategy()` to also quaff an unambiguous potion of speed when the wizard has visible monsters nearby and hitpoints are reasonably high (not about to die), prioritizing speed to improve survivability. This is one function rewrite, does not repeat any listed action, and should raise the score.

Change the bot from the proposal above. The judge measures that tree.
