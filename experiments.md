# Next experiment

## Proposal

Rewrite one function: `is_dangerous_monster` in
`autoascend/combat/monster_utils.py`.

## What it changes

The function currently calls a monster dangerous only when it is a pet or when its
name is in `INSECTS`. Every other monster is treated as safe until the wizard is
down to 8 hit points (`imminent_death_on_melee`). This is why the farm dies at
experience level 10 or 11: a hurt wizard (between 9 and 16 hit points) still walks
up to a dwarf lord, a rothe, or an orc and trades blows with it, and one or two
hits kill it. Those three names are exactly the parent's melee deaths on seeds 0,
1, and 13.

Add `'dwarf'`, `'rothe'`, and `'orc'` to the danger test:

```python
return is_pet or mon.mname in INSECTS or 'dwarf' in mon.mname or 'rothe' in mon.mname \
       or 'orc' in mon.mname
```

`'dwarf'` covers `dwarf lord`; `'orc'` covers `Mordor orc`. All three are slow
(speed at most 12), so the wizard can outrun them.

## Why it raises the score

`is_dangerous_monster` feeds three defensive behaviours:

- `imminent_death_on_melee` now returns true at 16 hit points for these monsters,
  so `draw_monster_priority_positive` stops drawing the approach ring and
  `draw_monster_priority_negative` draws the retreat ring.
- `get_potential_wand_usages` gives a 25-point bonus to zapping them with a wand.
- `elbereth_action` counts them toward the Elbereth threshold.

This matches the game rules: "A weak or slow monster is food more than a threat",
and the raised monsters are all slow. Above 16 hit points the approach is
unchanged, so the weak monsters that feed the farm are still killed. The parent's
last change did not touch this function and no listed action covers it.

## Boundaries

- Single function rewrite. No other file changes.
- The invisible Mordor orc (seed 9) is reported as `unknown`, so seed 9 is
  unaffected; the change targets the visible melee deaths.
- Soldier ants and fire ants are already in `INSECTS`, so they are unchanged.
