# Next experiment

## Result

- iteration 1: n/a not kept (net-zero on the public reference set; the judge's private
  seeds are different games). Rewrote `cast_attack_actions` in
  `autoascend/combat/fight_heur.py` so the wizard actually casts force bolt. The parent
  already carries the full gate (experience level 10+, the first dungeon level, spell
  known, fail chance <= 0.15, energy >= 10, one-turn cooldown) but returns the cast at
  priority 5, where thrown daggers (11), pickup (15), and melee (16) always win and the
  cast never happens. The rewrite keeps every gate, adds "only when there is nothing to
  throw", and raises the cast to priority 12 (still under pickup and melee) so it fires.

## The one change

Rewrite the one function `autoascend/combat/fight_heur.py::cast_attack_actions`.

The rules measure, as a raise: casting force bolt from experience level 10, on the first
dungeon level, at a monster that is not adjacent. As a lower: casting below level 10, off
the first dungeon level, at an adjacent monster, keeping less energy before the cast, or
withholding a throw because the bolt can go down that line.

The parent's function already enforces the xp / depth / distance / energy gates but is
neutered: `return [(5, ('cast', dy, dx, 'force bolt'))]` never gets selected, because
ranged (11) and pickup (15) beat it whenever they apply, and in the no-ammo situations
where they do not apply it still loses to the movement heatmap decisions (go_to is 1 but
the exploratory move choices are not on the same flat list). So the wizard throws away its
daggers and then walks into melee -- the deaths of seeds 0, 1, 5, 9, and 13.

The rewrite:

- keeps every parent gate (level >= 10, depth == 1, spell known, fail <= 0.15,
  energy >= 10, cooldown);
- refuses the cast whenever `ranged_priority` returns a throw (a dagger volley is kept, so
  no throw is ever withheld);
- keeps the 2..8 clear-line scan on a monster that is not in `WEAK_MONSTERS`; and
- returns `[(12, ('cast', dy, dx, 'force bolt'))]`, so the bolt fires when no throw is
  possible (ammo spent, or the target is past throw range) without ever overriding pickup
  (15) or melee (16).

Gates preserved verbatim: `experience_level < 10`, `depth != 1`, `'force bolt'` not a
known spell, `spell_fail_chance > 0.15`, `energy < 10`, and the `last_cast_fail_turn`
cooldown. Nothing else in the tree changes; the diff against the parent is confined to this
one function.

## Why the parent lost

See `experience.md`: after the daggers are spent, the late games (0, 1, 5, 13) and the
mid games (9, 14) die to a monster in melee or to one lucky hit, with no ranged option
left. The cast adds a ranged attack exactly there, gated so the games that die young
(below level 10) are untouched.

## Why it stopped

The parent batch is not in this note.