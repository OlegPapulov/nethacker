# Next experiment

## Proposal

Behaviour to add: **the wizard casts its attack spell (force bolt) at any
visible hostile monster within a clear line, from experience level 1 and on any
dungeon level -- not only at experience level 10+ on the first Doom level.**

Where: `combat/fight_heur.py`, `cast_attack_actions`. The function already
proposes force bolt, but two guards make it unreachable in the games that need
it:

```python
if agent.blstats.experience_level < 10:
    return []
if agent.blstats.depth != 1:
    return []
...
if agent.blstats.energy < 10:
    return []
```

Remove the experience-level gate and the first-Doom-level gate, and lower the
energy gate to the spell's own cost (5). Keep every other guard unchanged: the
line must be clear, the target must be a real hostile monster (not a weak
monster, not a pet, not a peaceful), the fail chance must be at most 0.15, and
the spell must not be re-offered for two turns after a failure.

Why this behaviour and not a number in a listed test:

- The listed tests tune *melee*, *movement*, *eating*, *prayer*, *Elbereth*,
  *wand path/zap penalties*, *skill points* and *corpse aging*. None of them
  mention the wizard's spell attack, so this is a behaviour the tests do not
  cover.
- The rules say a behaviour that starts at experience level 10 misses the games
  at 0.018, 0.024, 0.029 and 0.037 that die in the first few thousand turns.
  This behaviour starts at level 1.
- The wizard's energy has no other consumer in this agent (the healing casts
  are gated to the healer role and are commented out here), so casting is not
  competing with another emergency use -- it converts otherwise idle Pw into
  damage from a distance, which is the wizard's stated advantage.
- It is aimed squarely at the observed deaths: at levels 1-11 the wizard dies
  in melee to fast monsters it never gets to soften from range.

Expected effect: fewer melee deaths and more kills, so games that now stop at
Xp 8-11 should climb one or more experience levels. The early games gain a
level-1 ranged option; the deep games stop walking into melee with a full
energy bar. Risk is limited to the small nutrition cost of an extra cast and is
bounded by the unchanged line/fail-chance guards.

## Result

History of earlier attempts (mean of 15 seeds on `wiz-hum-cha-mal`):

- iteration 1: 0.063 not kept (no-cell-improved). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Lowered that threshold from weak to hungry.
- iteration 1: 0.064 not kept (no-cell-improved). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Raised several flee and Elbereth thresholds and ate more corpses from the pack.
- iteration 1/2: 0.064 not kept. No code change.
- iteration 1: 0.077 kept (registered). Capped a weak-hunger corpse walk at 20 squares.
- iteration 1/2: 0.077 not kept. Selected the wielded weapon's skill.
- iteration 1: 0.080 kept (registered). Latched onto dungeon level 2 when fainting and no edible corpse was within 20 squares.
- iteration 1: 0.114 kept (registered). Waited for experience level 12 before leaving the first Doom level.
- iteration 1/2: 0.114 not kept. Changed the launcher penalty.
- The current parent scores **0.1328** (per-seed table in `experience.md`).

The behaviour proposed above has not been tried before.
