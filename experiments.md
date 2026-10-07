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

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Change one test that already exists. Do not add a new action. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

## The proposal

One change: in `autoascend/combat/fight_heur.py`, `elbereth_action()` offers
`-15 + 20 * adj_monsters_count * (1 - player_hp_ratio)`. Raise the weight from
20 to 60, so the line reads
`return [(-15 + 60 * adj_monsters_count * (1 - player_hp_ratio), ('elbereth',))]`.
Nothing else changes. The gate `hitpoints < 30 and adj_monsters_count > 0`, the
constant -15, the `multiplier = clip(20 / hitpoints, 1.0, 1.5)`, every other
number in the file, and every other file stay exactly as the parent has them.

This is a change to a test that already exists. The `('elbereth',)` action is
already offered by `get_available_actions()` and already handled by
`_fight2_perform_action()`, which calls `engrave("Elbereth")`. No new action and
no new strategy is added; only the priority at which the existing engrave test
wins is moved.

Why this is the one to change:

- Eleven of the fifteen deaths were ordinary melee (killer bee, goblin, giant
  bat, plains centaur, vampire bat, newt, invisible Mordor orc, kitten, pony,
  kobold lord, dwarf lord). The measured reason nothing else can fix that is
  that melee is worth 16 and every movement tile is worth less: an earlier
  attempt that drew a negative ring for a fast adjacent monster changed no seed,
  because melee still won. The only action in `fight2` that beats 16 is
  engraving, because standing on the engraving takes 100 off the melee score and
  hands the turn to `wait_action`.
- With the weight at 20 the engrave test can never win the fights that kill the
  wizard. One ordinary monster scores 1.0 to 1.5 in `adj_monsters_count`, so the
  best reachable priority against one goblin or one giant bat is about 3, and
  only at about 6 hit points out of 40, against a melee of 16 and a
  repositioning move of about 10. It only wins against a monster
  `is_dangerous_monster()` scores at triple count (pets and insects), and never
  against the ordinary monsters in the death list.
- With the weight at 60 the same test fires inside the danger band and nowhere
  else: one ordinary monster at or below about 15 of 40 hit points (priority 16
  to 26), two ordinary monsters at or below about 22 of 40 (priority 16 to 20),
  one faster monster at or below about 22 of 40 (priority 16 and rising as the
  hit points fall). At full hit points the priority is still -15, so the wizard
  does not engrave when it is healthy and does not engrave when no monster is
  adjacent.
- The engine effects after the engrave are already built in and bounded. On the
  engraving the melee and ranged actions are worth -100, and `wait_action` is
  worth `30 - 40 * hp/max`, which beats every move tile while hit points are
  under roughly half of maximum, so the wizard waits on the engraving, takes no
  melee damage, regenerates, and steps back off above half. If the engraving
  is read back as Elbereth, `elbereth_action()` returns an empty list and the
  engrave is not offered again. If the read fails, the monster is repelled by
  the engraving and moves out of adjacency, `adj_monsters_count` becomes 0, and
  the engrave stops being offered as well. Either way the engrave loop ends
  after one or two turns instead of running away with the episode.

Why it is not one of the measured assumptions:

- The prayer wait, the prayer `hitpoints < 6`, the 20 square corpse walk, the
  melee `hitpoints > 8 or is_monster_faster()` test and the farm level latch are
  untouched. The `hitpoints < 30` engrave gate is untouched, so this is not the
  Elbereth threshold change that was raised before; the weight inside the
  priority is a different number in a different part of the test.
- The direction is the opposite of the measured melee change. Replacing the
  faster-monster test with a fatal-melee test made the wizard fight to the death
  and dropped the mean to 0.105. This change does not make the wizard attack
  more; it makes the wizard stop attacking, engrave, and wait, which is the
  untested direction.

Expected cost: one turn for the engrave and tens of turns per wait, paid only
when the wizard is already down to about 40 percent of its max hit points with a
monster adjacent, which is the state eleven of the fifteen seeds died in.

Change the bot from the proposal above. The judge measures that tree.
