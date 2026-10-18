# This gameplay

Identity: `wiz-hum-cha-mal`

## The one change

Rewrite `Agent.handle_exception` (autoascend/agent.py).

`handle_exception` is the one place every unexpected error in a strategy passes through.
Today it re-raises everything that is not an `AgentPanic`, and through `arena_adapter`
that is silent and terminal: the agent thread dies, `AutoAscendDriver.act` has nothing
left to hand the arena but ESC, no further game turn is ever played, and the run is cut
off at the no-progress abort with only what it had already banked.

The one recovery this agent already has is the one it wrote for `AgentPanic`: `main()`
logs it, steps ESC twice, calls `on_panic()` to re-read the observation, and re-enters
the global strategy. The change makes an unexpected error take that same recovery
instead of re-raising: log the `agent_panic` event, remember it in `all_panics`, and
return. `KeyboardInterrupt`, `AgentFinished` and `SystemExit` stay fatal. A loop that
keeps failing without taking a single game turn is still stopped, because main()'s
`inactivity_counter` raises a cyclic panic after five such recoveries.

The score is the maximum milestone a run ever reached, so a run that keeps playing
after a recovered error can only hold its score or raise it; it cannot fall. Seeds whose
runs never raise an unexpected error are untouched and replay byte-identically.

## History

- 0.064, kept: capped a weak-hunger corpse walk at 20 squares (0.064 -> 0.077).
- 0.077, kept: latched onto dungeon level 2 when fainting and no edible corpse within 20 (0.077 -> 0.080).
- 0.080, kept: waited for experience level 12 before it left the first Doom level (0.080 -> 0.114).
- 0.114: the mean today. The XP gate at 11, 12 and 14 gives byte-identical runs at 0.114, so no run reaches experience level 12 while farming.
- Left the score where it was: launcher-penalty edit (twice), spell-menu re-read, melee ring for a fast adjacent monster, hungry corpse walk 5->6/10, fainting corpse search 20->25, keeping only fire+magic traps out of the walk path, keeping the force bolt book in the pack on depth 1, dangerous-monster melee line 16->20.
- Lowered the score: visited unseen tiles before a search (0.077 -> 0.040), weak-hunger eat reordering, raising flee/Elbereth thresholds and eating more pack corpses, drinking below half HP, putting on a ring or amulet (0 -> every game ended in the first 14 turns).

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is 0.114 on `wiz-hum-cha-mal`. The games end on the first dungeon levels,
before the farm banks experience level 12.

## What might solve it

`experience.md` states no game end, so the one failure mode that is visible in the code
(not in the data) is the silent one: an unexpected error in a strategy kills the agent
thread, the arena then only ever receives ESC, and the run stops where it stood. The one
change is to give that error the same recovery the agent already uses for `AgentPanic`.

Change the bot from the proposal above. The judge measures that tree.
