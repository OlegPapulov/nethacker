# Next experiment

## What to try

Increase corpse search radius when hunger is weak or worse. In eat_corpses_from_ground (non-below-me case when hunger_state >= WEAK), change max_dist from 20 to 30. In has_edible_corpse_in_reach, change default max_dist from 20 to 30. This gives the bot a bit more reach to find food before starving on dlvl1 without being as aggressive as eating when merely hungry.

Rationale: preventing starvation on borderline seeds can improve the mean without hurting high-scoring seeds (must not reduce any seed at >= 0.179). The previous 20-square cap was what helped earlier; increasing slightly may rescue some runs.

## Proposed change (one test/threshold change)
- agent.has_edible_corpse_in_reach: default max_dist 20 -> 30
- agent.eat_corpses_from_ground: when hunger_state >= WEAK and not only_below_me, max_dist 20 -> 30

## Hypothesized effect
- Fewer starvation deaths on dlvl1; better chance to survive to reach/maintain XP. Mean score may increase slightly. No seed at 0.179+ should decrease.

Change the bot from this proposal.
