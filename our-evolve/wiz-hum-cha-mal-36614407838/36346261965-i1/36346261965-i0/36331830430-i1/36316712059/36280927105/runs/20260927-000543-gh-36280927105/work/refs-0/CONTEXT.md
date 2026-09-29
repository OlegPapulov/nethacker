# /refs/ — your reference material

Everything here is read-only.

- `parent/` — a pristine copy of the bot you're editing. `/workspace` started as a copy of this, so `diff -ru /refs/parent /workspace` shows exactly what you changed.
- `parent-eval.json` — the current bot's result on every seed: one row per seed with its `trajectory_id`, `character` (identity), `progress` score, deepest `milestone`, and `cause_of_death`.
- `attempts.md` — changes already tried, with the score each reached per identity.
- `attempts/<n>/` — the code for each recent tried change, each with its own per-seed `eval.json`.
