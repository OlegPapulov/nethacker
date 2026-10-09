# Next experiment

## Proposal: treat a wand of striking as an offensive wand

The parent's `Item.is_offensive_usable_wand` (in `autoascend/item/item.py`)
accepts only **ray** wands, so a **beam** wand of `striking` is never offered as
a `zap` even though the rest of the code already knows how to use it:

- `get_next_states` (`autoascend/combat/fight_heur.py`) already simulates a beam
  (`can_bounce = wand.is_ray_wand()`, with the `not can_bounce` branch returning
  the straight path);
- `Item.is_beam_wand` already lists `striking` among the beam wands, but that
  method is unused;
- the game rules name "a wand of striking" as a useful early find, and a wizard
  often starts with one.

Change: in `is_offensive_usable_wand`, keep a wand whose object is `striking` in
addition to the ray wands. The `no charges` guard, the `sleep`/`digging`
exclusions, the zap penalty of 15 and the pet-stop rule are all untouched, and
no listed test number changes.

Why this should raise the experience level: a wizard has very few hit points and
a poor melee score, so it loses melee trades. The most common death in the batch
is the killer bee -- fast and poisonous -- and the young deaths are to equally
ordinary monsters. A wand of striking gives the wizard a ranged attack in exactly
the games where it currently has no ray wand and must melee, letting it kill a
fast threat at 2-8 squares before the threat closes.

Checks run locally (no judge): `is_offensive_usable_wand` returns True for
`striking` and for the ray wands (`magic missile`, `fire`), and still False for
`locking`, `sleep`, `digging`, `polymorph` and `teleportation`. A 32,000-step
smoke run over four seeded wizard games that start with a wand of striking
offered the strike 1,153 times, zapped it, and raised no exception.

Risk: a beam does not bounce and the shared simulation does not stop it at the
first monster, so a target behind another monster can be slightly overvalued.
A zap is only fired when the beam path reaches a visible monster, so the charge
is not spent into empty floor.

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

The games are in `experience.md`. The batch dies young: four seeds stop at
experience level 2-6, and the most common killer is the killer bee.

## What is the problem

The current tree scores a mean of **0.1195** on `wiz-hum-cha-mal`. The bot is
kept only if the next mean is strictly higher. The wizard is a poor melee
fighter and throws away its one always-available early attack, the beam wand of
striking, because `is_offensive_usable_wand` accepts ray wands only.

## What might solve it

Add one behavior the listed tests do not already cover: use a wand of striking as
an offensive wand, so the wizard can kill a fast melee threat from a distance
when it has no ray wand. See the proposal above. Leave every listed test as it
is, including a nearby number in the same function. Do not change a number in an
existing test. Do not revert the change. The judge scores the tree you exit with;
a tree that matches the parent is not a result. The change is made in
`autoascend/item/item.py`. The judge measures that tree.
