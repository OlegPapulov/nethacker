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

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The score is the mean of the 15 judge seeds. Progress is the highest milestone a game reaches. Experience level moves that score. Seed 9 is at Xp:11. Seed 4 dies at 2,742 turns and stops at Xp:2. Seeds 10 and 12 die under 10,000 turns. Leave the weak-hunger corpse walk capped at 20 squares. Leave `_xp_farm_level` as it is. Leave `experience_level >= 12` as it is. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

## The one change

Farm the next Doom floor down when the floor under the wizard is used up.

Eleven of the fifteen seeds stop on one exact experience level, and no seed reaches
`Xp:12`. That is a stall, not a death: a stall is a loss here, and NLE ends an
episode after 10,000 steps with an unmoved turn counter. The XP farm parks the
wizard on Doom dlvl 1 until it is level 12, and a wizard with that floor dug out
has nothing left to do on it, so `current_strategy` spins in place and the run is
lost with whatever experience it had banked.

The change adds `GlobalLogic._floor_is_used_up()`, which asks directly what
`explore1` asks itself, from what the wizard already remembers:

- no unexplored stair (`get_unexplored_stairs(all=True)` is empty),
- no reachable tile left to walk to: `~level.seen & G.STONE` and un-kicked
  `G.DOOR_CLOSED`, expanded over the eight neighbours exactly as
  `explore1.to_visit_func` does, masked by `agent.bfs() != -1`,
- nothing left to search, by the same `search_diff > 400` yardstick `explore1`
  uses to decide the floor is dug out enough to walk across traps,
- and a way down that is actually achievable, so the target can be walked to.

When that holds on the floor the wizard is farming, the farm target moves to the
next Doom floor down, capped at `MAX_STALLED_FARM_LEVEL = 4`. Doom dlvl 1 has a
down stair (only the up stair is withheld), and the stairs strategy already in the
chain walks the wizard there, so this costs no new code path. The latch is cleared
as soon as the milestone leaves `BE_ON_FIRST_LEVEL`, and an `AgentPanic` from an
unreachable target falls back to the previous floor instead of ending the run.

Why this and not something safer: progress is monotone, so descending cannot cost
banked score, and deeper Doom floors are worth more experience per kill. The
detection is positive, so when it does not fire the behaviour is byte-identical to
the parent.

Change the bot from the proposal above. The judge measures that tree.
