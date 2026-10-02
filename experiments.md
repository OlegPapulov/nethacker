# Next experiment

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063). Raised several flee and Elbereth thresholds and ate more corpses from the pack.
- iteration 1: 0.0613 not kept. `imminent_death_on_melee` ordinary cut 8 -> 10 (the change asked for above), dangerous cut left at 16.
- iteration 2: 0.0635 not kept. Same cut 8 -> 6 instead. So the cut is already at its optimum: 6 -> 0.0635, 8 -> 0.0643, 10 -> 0.0613.
- iteration 1: 0.0595 not kept. `wait_action` in `combat/fight_heur.py` returns nothing while a monster is adjacent (Elbereth cannot dislodge one) plus the same guard in `elbereth_action`. The bot turns aggressive and four seeds then die to a white unicorn.
- iteration 2: 0.0569 not kept. The same guard alone on 15 seeds.
- iteration 1: 0.0467 not kept. `to_search_func` in `exploration_logic.py`: search bonus 250 -> 128 (about 8 searches per square instead of 11).
- iteration 2: 0.0595 not kept. Search bonus 32 (about 4 searches per square); seed 13 survives 34703 turns instead of 19144 but only reaches Xp:9 instead of Xp:7, i.e. the extra turns do not convert into XP. Search bonus 8 is 0.0524.
- iteration 1: 0.0602 not kept. `eat_corpses_from_ground` triggered at `Hunger.HUNGRY` instead of `Hunger.WEAK`, with the distance cap at 3 / 10 / unlimited (identical results). Walking to corpses earlier costs more turns than the nutrition is worth.

## Why it stopped

died of starvation (1 of 15).

## What is the problem

Mean progress is 0.064. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.
Baseline 0.06431 over the 15 public local seeds, reproduced exactly (`/home/agent/h/peval.py 0 15`).

## What is known now (all measured on 15 seeds)

- Cause of death, in order of frequency: starvation/fainting (4 of the 6 weakest seeds), then a
  single losing melee trade at near-full HP, then the occasional shopkeeper/pony/unicorn.
- The 6 weak seeds are 4 (2644 turns, Xp:2), 8 (4142, Xp:3), 12 (4917, Xp:4), 14 (7795, Xp:5),
  5 (8788, Xp:6) and 11 (12486, Xp:6). Five of the six never leave dungeon level 1.
- Seed 12 spends its last 250 turns in a faint/regenerate loop at 5-30 HP out of 36, dying to a bat.
  Seed 4 faints at turn 2630 and dies at 2644 to a kobold zombie while fainting.
- Median HP ratio over a game is 1.0. There is no slow chip damage; the bot heals fully between
  fights. Failures are one burst from full HP followed by a slow, losing recovery.
- Natural regeneration is 1 HP per ~5 turns and the bot never sleeps, so recovery from a burst
  takes 200-900 turns.
- `on_elbereth_frac` is 0.004 or less; the bot almost never gets an Elberenguard up, so it heals
  in the open.
- Ground corpses are only considered edible for 50 turns after the kill
  (`_is_corpse_editable`), and a human wizard cannot eat humanoid corpses (M2_HUMAN), so its
  entire food supply on dlvl 1 is fresh jackal/fox/lizard/rat corpses it personally saw created.
  Carrying corpses instead was tried: it avoids the stale window but carried corpses still rot,
  and seed 5 was then poisoned by a rotted giant rat corpse.

## What might solve it

Nothing in the combat/aggression/hunger/search axes moved the mean: every direction tried is
worse than the baseline, and the melee cut in `imminent_death_on_melee` is at a local optimum.

The two levers that are still untried and are not more of the same:

1. **Actually use the character.** The wizard finishes games at experience level 8-9 with 61
   energy and `known_spells` empty, so it never casts and never uses `Agent.cast`. Nothing in the
   code reads a spellbook. On dlvl 1-2 even one spell (magic missile, sleep, healing) would beat
   the 1d4+2 dagger trades that kill it. `character.parse_spellcast_view` and `Agent.cast` exist
   and are unused. Note the earlier probe: a fresh wizard knows no spells and finds no spellbook.
2. **Sleep.** Nothing in `autoascend/` ever sleeps. Falling asleep heals far faster than the
   1 HP/5 turns the bot currently gets, which is exactly the resource missing in the terminal
   low-HP phase that kills seeds 3, 0 and 12. It needs a safe square and a wake-up condition,
   so Elbereth coverage (`can_engrave`) is the natural safe spot.

Do not re-try the search budget, the melee/flee thresholds, the adjacent-monster guard, or
earlier corpse eating; all were measured and are worse.
