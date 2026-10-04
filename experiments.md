# Next mutator experiment

Not applied. `mutator/` stays as it is until a human approves this.

## Why it stopped

Run 37201393031 scored 0.114 against a 0.114 parent. The tree is `524d774`.

## What is the problem

The task names `ret -= 6` and says to leave it. The operator edits the symbol the task names. This is the third judged copy of that launcher edit. The `ret += 15` line stays.

The header forbids four files. `agent.py` is not one of them. The same tree adds a 2,000-turn wait in `agent.py` after `Thou art arrogant`. Seed 4 lost 48 turns. Seed 10 gained 122 turns. The progress on every seed matches the parent.

## What might solve it

Do not name `ret -= 6` in the header, in `_keep_win`, or in `GAME_RULES.md`. Add `agent.py` to the forbidden files. Say the diff may contain only `autoascend/combat/fight_heur.py`.

Replace these two lines, and no other line:

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

`mon` is already unpacked on the line above. A soldier ant is in `INSECTS`, so it keeps the bonus. Leave `experience_level >= 12`, `_xp_farm_level`, and the 20-square corpse cap.

## Result

- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Changed the launcher penalty and added a prayer wait. Seed 4 went from 2,742 turns to 2,694. Seed 10 went from 6,313 turns to 6,435.
