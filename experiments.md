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

## Last iteration

The parent scored 0.114 and is kept. Do not submit any of the diffs listed above
again; in particular do not re-add force bolt to `emergency_strategy` (measured
0.0532 with, 0.0694 without), do not widen the 50-turn corpse window (0.0496 at
500), and do not touch the corpse walk, `_xp_farm_level` or the `Xp >= 12` gate.

## Why it stopped

The previous tree scored 0.114 and was not improved on. The recorded attempts
clustered on the food axis and every one of them lost or was flat, so the axis is
exhausted. The remaining loss is on the combat axis.

## What is the problem

Progress is the maximum milestone ever seen, and for this wizard the XP ladder is
worth far more than the depth ladder (`Xp:11` = 0.2548, `Dlvl:12` = 0.2061,
`Xp:14` = 0.4940). The batch's ceiling is `Xp:9-11`: seed 9 banks `Xp:11`, seeds
10/12/4/8 die under 10,000 turns, seed 4 dies at 2,742 turns still on `Xp:2`.
The gate at `Xp >= 12` never fires, so nothing is reaching it.

`combat/fight_heur.py` writes Elbereth and then obeys it in a way that is
unconditional and self-inflicted:

* `elbereth_action` only offers the engraving when a monster is **already
  adjacent** and `hitpoints < 30`. At full health `adj_monsters_count` is scaled
  by `1 - sqrt(hp/max) == 0`, so the priority is `-15` and it never fires; and a
  wizard's `max_hitpoints` is under 30 anyway. The words are therefore *only*
  ever written while damaged and with something next to us.
* `wait_action` then returns `30 - 40 * hitpoints / max_hitpoints` while the
  engraving is underfoot, and `get_available_actions` /
  `get_potential_wand_usages` subtract 100 from `melee`, `ranged` and `zap`. The
  strongest remaining action is a `move` worth at most 3 (`go_to` 1, `melee`
  -84, `ranged` -89, `zap` -100), so **below two thirds of its hitpoints a
  wizard that has written Elbereth is frozen**: it cannot strike, shoot, zap or
  walk away.
* `fight2` only returns when nothing is within seven squares, and it is preempted
  above `emergency_strategy`, so nothing downstream can break the loop. The
  monsters keep hitting for free until it dies, banking no experience.

For `max_hitpoints` 20 with two dangerous monsters adjacent the engraving is
offered from 13/20 hitpoints down and is the top action from 14/20 down; a
dangerous+plain pair needs 11/20 and two plain monsters 4/20. That is the middle
of an ordinary first-floor fight. The bot can only do this while holding a marker
or pointed tool, which is why the cost is spread across seeds rather than
uniform.

This matches the recorded signature: games that stop early (`Xp:2` after 2,742
turns) and an XP ceiling that extra farming never breaks.

## What might solve it

**One change: refuse to write Elbereth while damaged.**

In `autoascend/agent.py`, `Agent.can_engrave` now returns False when
`self.blstats.hitpoints < self.blstats.max_hitpoints`. `can_engrave` has exactly
one live caller, `combat.fight_heur.elbereth_action` line 204, so the guard
removes the engraving offer from the moment it would be made and from every
moment after. `fight_heur.py`, `exploration_logic.py`, `fight2`,
`emergency_strategy`, the 20-square corpse walk, the `_xp_farm_level` fainting
test and the `experience_level >= 12` gate are all untouched.

Why this and not another Elbereth threshold: the paralysis is not a tuning
problem, it is a sign error in the policy. `wait` is meant to be the low-priority
fallback, and it is handed the *highest* priority in the whole fight for any
character below two thirds of its hitpoints, while every offensive action is
handed `-84` or worse. No threshold on `hitpoints < 30` or on `adj_monsters_count`
fixes that, and raising them was already measured as flat (0.077, "raised several
flee and Elbereth thresholds").

Why the guard is `hitpoints < max_hitpoints` and not a number: it is the exact
boundary at which `wait` starts outranking movement, expressed without a
hardcoded 30 that only suits this character's `max_hitpoints`. It is a role- and
race-neutral statement -- "do not write a message that stops you fighting while
you are already losing" -- so it holds for every legal character, not just
`wiz-hum-cha-mal`, and it leaves the engraving available to a character standing
at full hitpoints where `wait` is worth `-10` and costs nothing.

Expected effect: runs that froze mid-fight on the first Doom floor go back to
trading hits. Those runs bank experience instead of stopping, and because
progress is a running maximum, every extra level is worth 0.02 to 0.13 on that
seed directly. Seeds that never pick up a marker are unaffected, so the downside
is bounded at zero and the upside is several experience levels on the seeds that
do.

Describe the games in `experience.md`. Propose one change in this file, in
accordance with the game rules. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
