# Next mutator experiment

Applied with this change.

## Why it stopped

Run 36951341311 scored 0.064 and 0.063 against a 0.064 parent. Neither was kept. The seed was this owner's best public bot for `wiz-hum-cha-mal`.

## What is the problem

The first edit cannot execute. It caps non-local corpse walks at 3 squares when hunger is below weak. Those walks are already called only when hunger is at least weak, so the 15 seeds replayed the parent exactly (0.06431333032572426). That attempt took 166 minutes and 4.9 million tokens.

The second edit moved five combat numbers at once and started eating any safe corpse from the pack. The long games got shorter. Seed 6 went from 0.117 at depth 5 to 0 in 1,289 turns. Seeds 4, 8, 11, and 12 got deeper. The mean fell by 0.002.

`mon in WEAK_MONSTERS` compares a monster record to a list of names, so it is always false. The second edit changed it to `mon.mname` inside the same diff. That is a real behavior change buried under the threshold edits.

The playthrough header still says the usual stop is a jackal, because that death appears twice. One game still starves. The agent treated the jackal line as the task.

## What might solve it

The note for the next run names one function and forbids a second. Do not edit `eat_corpses_from_ground`. Change only `imminent_death_on_melee` in `autoascend/combat/monster_utils.py`: raise the ordinary cut from 8 hit points to 10, and leave the dangerous-monster cut at 16. Do not edit Elbereth, melee priority, flee radii, or `eat_from_inventory`.

## Result

- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063). Raised several flee and Elbereth thresholds and ate more corpses from the pack.

## Result

- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064).
- iteration 2: 0.064 not kept (no-cell-improved). Does not change the mean (0.064).

## Proposal (not approved)
Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.

# Next experiment

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063). Raised several flee and Elbereth thresholds and ate more corpses from the pack.

## Why it stopped

died of starvation (1 of 15).

## What is the problem

Mean progress is 0.064. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

One game still starves. The parent already walks to a corpse once hunger is weak. Do not edit `eat_corpses_from_ground`. A distance cap there never runs, and eating sooner shortens the long games. Change only `imminent_death_on_melee` in `autoascend/combat/monster_utils.py`: raise the ordinary cut from 8 hit points to 10, and leave the dangerous-monster cut at 16. Do not edit Elbereth, melee priority, flee radii, or `eat_from_inventory`.

Edit `autoascend/` and exit. The judge measures that tree.

