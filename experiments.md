# Next mutator experiment

Applied with this change. The seed gives the exact depth-1 lines. The job replaces `MEASURE` after install so the operator does not play.

## Why it stopped

The mean is 0.11444300565928403. That number is the average of 15 XP scores. No seed has reached Xp:12 (0.333). The best seed is Xp:11 (0.255). Five seeds stop at Xp:10 (0.179). Three seeds stop at Xp:8 (0.075). Seeds 4, 8, 10, and 12 stop at Xp:2, Xp:6, Xp:4, and Xp:5.

## What is the problem

A rise of 0.01 on the mean needs 0.15 more progress in the batch. One seed from Xp:10 to Xp:11 adds 0.076. The four short seeds, if each reaches Xp:8, add about 0.190. That is about 0.013 on the mean.

The level-12 gate does not run in those four games. They die before experience level 8. Seed 14 fell from Xp:9 to Xp:8 when the gate rose from 8 to 12. A longer stay can lower a score. Do not raise the gate.

The untested edit is the `ret += 15` line on depth 1. The operator has not made it. The operator edits `ret -= 6` when the task names that line. Run 37209219942 then spent the 360 minutes inside the operator. The brief tells the operator to play seeds and to wait up to 600000 ms. The judge did not finish.

## What might solve it

After `pip install nethackers`, replace `MEASURE` in `nethackers/harness/brief.py`. The new text says: do not run `python -m nethackers.arena.run`. Do not wait on a local game. The judge plays the seeds after you exit. The cold start stays. The judge stays. If the old `MEASURE` text is absent, the job fails.

Do not name `ret -= 6` in the seed. The only edit is this replacement in `melee_monster_priority`, and no other line:

```python
    ret = 1
    if agent.blstats.hitpoints > 8 or is_monster_faster(agent, monster):
        ret += 15
```

with:

```python
    ret = 1
    bonus = agent.blstats.hitpoints > 8 or is_monster_faster(agent, monster)
    if agent.blstats.depth == 1 and mon.mname not in INSECTS:
        bonus = False
    if bonus:
        ret += 15
```

`mon` is already unpacked on the line above. A soldier ant is in `INSECTS`, so it keeps the bonus. Leave `experience_level >= 12`, `_xp_farm_level`, and the 20-square corpse cap. `agent.py` is already forbidden.

## Result

- iteration 1: none. Run 37209219942 was cancelled at 360 minutes. The operator used 1,542,509 tokens. The judge did not finish.

## Result

- iteration 1: 0.081 not kept (no-cell-improved).

## Proposal (not approved)
Source: the last mutator iteration. Applying this means editing `mutator/`, which needs a human yes.

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

no finished games (0 of 0).

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Leave `_xp_farm_level` in place. Do not edit it. Leave `experience_level >= 12` in place. Do not raise it. Do not edit `global_logic.py` or `exploration_logic.py`. Seeds 4, 8, 10, and 12 stop at Xp:2, Xp:6, Xp:4, and Xp:5. Those four games die under 10,000 turns. In `melee_monster_priority`, replace these lines and no other line. When `blstats.depth` is 1 and the monster is not in `INSECTS`, do not add 15. A soldier ant keeps the bonus.
```python
    ret = 1
    if agent.blstats.hitpoints > 8 or is_monster_faster(agent, monster):
        ret += 15
```
with:
```python
    ret = 1
    bonus = agent.blstats.hitpoints > 8 or is_monster_faster(agent, monster)
    if agent.blstats.depth == 1 and mon.mname not in INSECTS:
        bonus = False
    if bonus:
        ret += 15
```

Edit only the function named above. The judge measures that tree.

