# Next mutator experiment

Applied with this change. A tie keeps the checkout. The seed says to copy the second block and names no other condition.

## Why it stopped

Run 37233060279 scored 0.08065773574577405 against a 0.114 parent. The tree is `43076a3`. The parent seed is `524d774`.

## What is the problem

`best_public` uses `>`. A tie keeps the first hub row. That row was `524d774`, an unkept tree with the same 0.114 score as the checkout. The run then edited that tree, not the kept bot.

The task showed the exact depth-1 block. The task also said "do not add 15". The operator wrote a different test: monster difficulty at most the experience level, and 21 when the monster has no difficulty. Versus `524d774`, that test is the only new code.

Seed 8 rose from Xp:6 to Xp:10. Seed 9 fell from Xp:11 to Xp:5. Seeds 4, 10, and 12 did not move. The mean fell by about 0.034. The brief patch did work. The operator ran for 1,695 seconds.

## What might solve it

On a tie, use the checkout. The checkout is the kept bot.

In `_keep_win`, show the two blocks and one order: copy the second block over the first, and change no other line. Remove the sentence "do not add 15". Do not name difficulty in the seed. A different condition on that line scored 0.081.

Leave `experience_level >= 12`, `_xp_farm_level`, the 20-square corpse cap, and the `MEASURE` patch.

## Result

- iteration 1: 0.081 not kept (no-cell-improved). Decreases the mean by 0.034 (from 0.114 to 0.081). Replaced the bonus test with monster difficulty. Seed 8 rose from 0.037 to 0.179. Seed 9 fell from 0.255 to 0.029.

## Result

- iteration 1: 0.079 not kept (no-cell-improved).
- iteration 2: 0.065 not kept (no-cell-improved). Decreases the mean by 0.013 (from 0.079 to 0.065).

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

## Last iteration

The previous tree scored 0.079 and was not kept. Do not submit that same diff again.

## Why it stopped

no finished games (0 of 0).

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. Leave the weak-hunger corpse walk capped at 20 squares. Do not edit it. Leave `_xp_farm_level` in place. Do not edit it. Leave `experience_level >= 12` in place. Do not raise it. Do not edit `global_logic.py` or `exploration_logic.py`. Seeds 4, 8, 10, and 12 stop at Xp:2, Xp:6, Xp:4, and Xp:5. Those four games die under 10,000 turns. In `melee_monster_priority`, copy the second block over the first. Change no other line.
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

