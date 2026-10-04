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
