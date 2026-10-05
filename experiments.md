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

## Proposal (this iteration): cast at range instead of walking into melee

The fifteen parent games all die on the Dungeons of Doom at `Xp:8`-`Xp:11`, and
the `death=` column of `/refs/parent-eval.json` says why: three die to a goblin,
a kitten and a newt, five more to monsters the agent's own
`is_monster_faster` calls faster than the wizard (killer bee, giant bat, vampire
bat, pony). A chaotic human wizard at `Xp:3` has about five hit points,
`emergency_strategy` only drinks a *identified* healing potion and only below a
third of maximum, and it cannot heal its way out of that. It has one attack --
walk adjacent, swing the knife, take a hit back -- and no second one. Every
caster line in `emergency_strategy` is commented out, so `cast()` is never
called even though `main()` already reads the cast menu and
`character.known_spells` is full.

**Change:** add `Agent.cast_at_monsters()`, a strategy that fires the character's
cheapest attack spell at a monster that is two to six squares away, and give it
priority over `fight2()` in `global_logic.global_strategy()`.

Why this and not a retreat heuristic: the parent already has a good melee
heuristic (`fight_heur.py`, which this edit may not touch), and it gives melee
priority 16 whenever the wizard is above 8 hit points because on a healthy
wizard that trade is correct. The bot is not losing because it fights; it is
losing because when a monster is two to six squares away it *walks toward it*
with no option but the knife. Substituting a cast for that walk is not a
substitution at all -- it is the same turn, spent on damage instead of on
closing -- so this cannot cost experience the way a flee rule would, and it
removes the approach that produces "killed by a newt at one hit point". It is
also the character's identity: the rules say a spell does damage from a
distance, and this bot never casts one.

Details that matter:

- The target is chosen from `get_visible_monsters()` (already excludes pets and
  the peaceful), skipping `ONLY_RANGED_SLOW_MONSTERS`, which never close, and
  only off-axis monsters, because `calc_direction()` asserts a target is in one
  straight line and `getdir()` accepts one direction per cast.
- Distance 1 is excluded: that is a melee fight `fight2` can already win with a
  free knife, and casting there would only spend the energy a monster that came
  to us did not deserve.
- The spell is picked from the game's own cast menu, by
  `spell_category == 'attack'` -- the word the menu prints next to the spell --
  never from a guessed name or a hardcoded letter. Cheapest (`spell_level`)
  first, because magical energy is the wizard's scarcest resource and the parent
  notes put its refill at about fifty turns; magic missile costs a handful of
  energy, never fails, and at `Xp:10` is already a multi-dart ray.
- Spells above 15% failure are skipped; `SPELL_REFUSED_MESSAGES` in `cast()`
  already turns a refusal into a wait instead of a lost menu.
- Energy is gated at `max(3, spell_level + 4)`, matching the `energy >= 5`
  convention `should_cast_heal()` already uses for a level-1 spell.
- The menu is re-read at most once every 200 turns, and only when a cast is
  actually wanted and the known spell set cannot pay for one, so the two turns
  the read costs are never spent on a floor with no use for them. A wizard gains
  a spell every level or two and `main()` reads the menu once, at turn 0.

Untouched on purpose: the corpse walk capped at 20 squares, the
`experience_level >= 12` gate, the fainting test that sets `_xp_farm_level` to 2,
`fight_heur.py`, `exploration_logic.py`, `fight2`, `emergency_strategy`. The
wizard still farms dlvl 1 and still dies on it; it just no longer walks into the
fight with nothing in its hand.

## Why the previous tree stopped

The parent sits at mean **0.1144** on the fifteen judge seeds. It stopped there
because the `Xp:12` gate it farms toward is never reached -- the best game in the
batch banks `Xp:11` and stops -- so the bot never leaves the Dungeons of Doom,
never meets a depth milestone worth more than 0.0265, and dies on floor one
after 2,742 to 73,840 turns of knife-only combat.

## What is the problem

Mean progress is 0.1144. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The score is the mean of the 15 judge seeds. Progress is the highest milestone a
game reaches, and on every parent seed that milestone is the experience level, so
the only thing that moves the mean is surviving longer on the Doom floors.
Turns and experience are almost a straight line across the batch (2,742 turns ->
Xp:2; 9,957 -> Xp:6; 23,577 -> Xp:8; 69,906 -> Xp:11), and seeds 4, 10, 12 and 8
die inside 10,000 turns at Xp:2/4/5/6 -- 0.040 of the 0.065 gap between this
mean and an all-`Xp:10` mean. Leave the weak-hunger corpse walk capped at 20
squares. Leave `_xp_farm_level` as it is. Leave `experience_level >= 12` as it
is. Give the wizard its one ranged attack instead of another knife trade.

Change the bot from the proposal above. The judge measures that tree.
