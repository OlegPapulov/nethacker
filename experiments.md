# Next experiment

## Result

- iteration 1: 0.114 kept (registered). The parent batch. Waited for experience
  level 12 before leaving the first Doom level; the latch already sends a
  fainting wizard with no edible corpse within 20 squares down to dlvl 2.

## Why it stopped

The parent batch is mean 0.114 on `wiz-hum-cha-mal`. Most seeds die at
`Xp:8` on dlvl 1–2, and seed 14 regressed (0.117 -> 0.075) when the gate kept
it on dlvl 1. The score is the peak experience level, so the Xp 8 runs are
the lost points.

## What is the problem

At WEAK the wizard walks up to 20 squares to eat a corpse (the 20-cap is
load-bearing). At FAINTING the latch only descends to dlvl 2 when there is no
edible corpse within 20 squares. A seeding wizard that is fainting but keeps
failing to reach a corpse at distance 11–20 (path blocked, corpse vanished or
rotten by arrival) retries the doomed walk over and over, stalls at `Xp:8`,
and dies. The corpse-walk cap (in `eat_corpses_from_ground`) is not the
problem; the latch's reach test — `has_edible_corpse_in_reach(max_dist=20)` —
fires too late to rescue that stall.

## What might solve it

Change one existing test: the dlvl-2 food latch in `current_strategy`.

- Before: when hunger reaches FAINTING and `not has_edible_corpse_in_reach()`
  (default `max_dist=20`) on the first Doom level, latch the farm level to 2.
- After: the same latch with `max_dist=10`. A wizard that is fainting and has
  no edible corpse within 10 squares goes down to dlvl 2, instead of walking
  11–20 squares to a corpse it keeps failing to eat while fainting.

This is in the same direction as the two kept changes that built the current
mean (cap the weak-hunger corpse walk at 20, latch to dlvl 2 when food-starved)
and it is strictly rescue-only: any corpse within 11–20 that is actually
walkable is still eaten first, because the eat preem comes before
`current_strategy` (the latch) on that turn. The change only fires when that
nearby-but-not-really-attainable corpse would otherwise send the wizard into a
fainting corpse-race. A fainting walk is a documented death (a faint next to a
monster is a death), so substituting a descent to a fresh floor that has its
own monsters and corpses should turn the `Xp:8` stall runs into runs that
reach `Xp:9`/`Xp:10`.

No new action is added; only the reach of the latch test changes.

Change the bot from the proposal above. The judge measures that tree.