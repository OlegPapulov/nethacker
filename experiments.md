# Next experiment

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063). Raised several flee and Elbereth thresholds and ate more corpses from the pack.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The tree matches the seed.
- iteration 2: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The agent wrote a notebook and left the parent in place.
- iteration 1: 0.077 kept (registered). Increases the mean by 0.013 (from 0.064 to 0.077). Capped a weak-hunger corpse walk at 20 squares.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). The judge table matches iteration 1.
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). No code change.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Read the spell menu and deleted the cast.
- iteration 1: none not kept (gate:child identical to parent). The tree matched the parent, so the judge did not run.
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Resubmitted the spell-menu tree. The 15 seeds match the parent.
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Drew a negative ring for a fast adjacent monster. The 15 seeds match the parent, because melee is still worth 16.
- iteration 1: 0.040 not kept (no-cell-improved). Decreases the mean by 0.037 (from 0.077 to 0.040). Visited unseen tiles before a search. Seeds 10 and 12 rose. Seed 13 fell from 0.179 to 0.024.
- iteration 1: 0.080 kept (registered). Increases the mean by 0.003 (from 0.077 to 0.080). Latched onto dungeon level 2 when fainting and no edible corpse was within 20 squares. The melee function did not change.
- iteration 1: 0.114 kept (registered). Increases the mean by 0.034 (from 0.080 to 0.114). Waited for experience level 12 before it left the first Doom level. Seeds 4, 8, 10, and 12 did not change. Seed 14 fell from 0.117 to 0.075.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Changed the launcher penalty. The 15 seeds match the parent.
- iteration 2: none. The job was cancelled at 360 minutes. No score.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Submitted the launcher edit again. The 15 seeds match the parent.
- iteration 1: new. Added `avoid_overload` (GlobalLogic). When NetHack reports the wizard at Strained (3) or worse on `blstats.carrying_capacity`, it drops the heaviest item the wizard is neither wearing nor wielding -- corpses first -- once per turn until it can move and fight again. Reactive only: it is a byte-for-byte no-op whenever the wizard is Burdened (1) or unencumbered, which is every game that does not lose a polymorph (lycanthropy) and get trapped Overloaded in a tiny form. Local core seed 15 rose from Xp:5 to Xp:6; seed 10 kept Xp:9 and spent fewer turns Overloaded. Not yet judged.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher.

The one function to add is `avoid_overload` (a `GlobalLogic` strategy, wired into `global_strategy` just below `engulfed_fight` and `emergency_strategy`).

Hypothesis: the one avoidable death found in the ends of the games (`experience.md`) is being Overloaded while polymorphed. Lycanthropy turns the wizard into a wererat (corpse weight 40, physical size tiny) on a timer; NetHack then rescales carrying capacity to the tiny form, so the wizard's ordinary pack is past three times what it can carry. `arrange_items` refuses to manage items while polymorphed, so nothing sheds the weight, and NetHack refuses both fighting and movement until the wizard is dead.

NetHack publishes the ground truth the item model is missing: `blstats.carrying_capacity` is `near_capacity()` (0 unencumbered .. 5 Overloaded). `avoid_overload` reads it, and at Strained (3) or worse drops the heaviest item the wizard is neither wearing nor wielding (corpses first, then spare weapons), re-reading the inventory first so an item picked up on the previous turn is seen, and repeats on following turns until the level falls back. It is placed below the emergency and engulfed strategies so prayer and escaping a stomach still win, and above `fight2`, because a heavily loaded wizard cannot attack anyway.

Acting only at Strained+ is deliberate: Burdened (1) and Stressed (2) merely slow the wizard down, and shedding gear there cost games (it threw away the spare weapon and shield it later needed). The change is inert -- identical actions -- on every game that never reaches Strained, so it cannot lower the mean; it can only matter where the wizard was already helpless.

The task is one change: add `avoid_overload`.

