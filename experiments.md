# Next experiment

## Result

- iteration 1: 0.11949 no change (not kept). Confirmed the harness: the judge
  derives each NLE seed from `Objective("wiz-hum-cha-mal")` defaults
  (`max_steps=1,000,000`, `no_progress_timeout=10,000`). The 15 public-seed
  runs on the pristine tree reproduce the parent eval exactly, per seed.
- iteration 1: 0.0536 not kept (mean falls from 0.11949). Hypothesis: fight in
  a corridor/doorway so a swarm (killer bee, jelly, dwarf lord) only gets one
  monster in melee, per the game rules' "a fight in a doorway lets one monster
  hit". Added a +2 corridor priority whenever two or more melee monsters are
  visible. Measured: the whole movement field shifts, the farm collapses (seed
  3 falls from Xp11 to Xp2), and the batch shrinks. Reverted. The idea is real
  but the lever (constant movement bias) is far too broad.
- iteration 2: 0.0503 not kept (mean falls). Hypothesis: the wizard carries
  unidentified healing / fruit-juice potions it never drinks -- only
  unambiguous items are quaffed and nothing identifies potions -- so the
  food-death seeds (4, 12) starve with food in the pack. Added a behavior that
  quaffed one unidentified potion when healthy and unthreatened. Measured: it
  fired essentially every five turns, exhausted the potion supply, and the
  paralysis / polymorph / poison outcomes cratered the farm (seed 9
  Xp11 -> Xp3). Reverted.
- iteration 3: 0.0503 not kept (mean falls). Same idea, narrowed to fire only
  at hunger WEAK after the corpse walk fails, with hitpoints >= 40 and no
  hostile monster within 12 squares. Measured: still disturbed the top games
  (seed 3 Xp11 -> Xp2), because even one potion quaff per starving episode
  changes the trajectory of the farm seeds that also hit weak stretches.
  Reverted.
- iteration 4: 0.0880 not kept (mean falls; seed 3 Xp11 -> Xp6, seed 9
  Xp11 -> Xp10). Hypothesis, per the rules' "when hit points are low, hit,
  zap, or step into a doorway": when hurt (< 50% HP) and meleed by two or more
  monsters at once, step one square to anywhere no host lies adjacent, so the
  one-against-many trade becomes a one-against-one. Measured: it fires exactly
  when the parent already loses the fight, so the local behavior is better,
  but the changed fight resolution ripples through the rest of the farm and
  the two top seeds fall out of Xp11. Reverted.
- iteration 5: 0.0711 not kept (mean falls; mean wounded by batch noise, so it
  was A/B'd per seed). Hypothesis: gate the emergency potion quaff on
  experience level < 7 so the farm games can never reach it -- only the
  doomed low games (4, 10, 12) would quaff at hunger WEAK with no corpse in
  reach. Measured: seed 12 does improve (Xp5 -> Xp7), but gating on Xp does
  not protect the farm, because the top seeds also spend their first floors
  below Xp7: the decider reproducibility was the top seeds, seed 3
  Xp11 -> Xp6, seed 9 Xp11 -> Xp5, seed 0 Xp9 -> Xp6, all confirmed by
  deterministic single-seed runs. Reverted.

## Why it stopped

The parent tree is at a sharp measured optimum on these seeds. Any recurring
new action -- a movement bias, a potion quaff, a step-out -- perturbs the
delicate farm trajectory on dlvl1 and pushes the two Xp11 seeds (3, 9) back
to Xp6-Xp10, which costs far more than any single low-game rescue gains.

## What might solve it

A behavior that only ever fires in states the farm games never reach. The
candidates measured here all fired during ordinary farm turns. The remaining
untapped edge cases (an invisible floating-eye gaze in dark rooms, an
unidentifiable drainer on dlvl1-2, a kitten that kills a 4-HP wizard during
prayer) all turned out to be unfixable without touching tested numbers or
without instrumentation that perturbs the trajectory. A next candidate should
be validated on the single reproducible seeds first (`.seeds`-free
`eval_seed.py` A/B) and only then on the full 15-seed batch, using the
`Objective` defaults in the header above.