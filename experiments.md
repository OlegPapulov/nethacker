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

Every seed is lost to a monster (see `experience.md`). The four seeds that bank
Xp:11 die on the first Doom level to one dangerous monster each: a dwarf lord, a
fire ant, a soldier ant, and an invisible Mordor orc. Two of those four are ants.

## What is the problem

Mean progress is around 0.1379. The bot is kept only if the next mean is strictly
higher on `wiz-hum-cha-mal`. The wizard has few hit points and its only ranged
attack is force bolt, which is gated to the farm floor; once a monster is in
melee range the fight is close.

## What might solve it

### Proposal: rewrite `melee_monster_priority` (in `autoascend/combat/fight_heur.py`)

Keep the melee bonus for a monster that is actually faster than the wizard, not
only for the handful of monsters whose names happen to be on the hand-written
list.

The fire ant and the soldier ant that end seeds 3 and 5 have `mmove` 18 against
the wizard's 12, so they are genuinely faster. `combat/monster_utils.is_monster_faster`
is name-based (it carries a `# TOOD: implement properly` note) and misses the
ants, so at low hit points `melee_monster_priority` withdraws the `+15` melee
bonus from an ant and the wizard tries to walk away. A faster monster closes
again on the same round and attacks again while the wizard only walks, so the
turn buys no damage and no escape. The rules agree: a faster monster takes its
turn before the wizard, and dropping the melee bonus for a faster monster lowers
the score. Standing and trading is already what the parent does above 8 hit
points and for the named fast monsters.

The change is one condition in `melee_monster_priority`: add `or mon.mmove > 12`,
using the monster's real permonst speed (the same `mmove` field the movement
heatmap already keys on) so any monster that can outrun the wizard keeps the
bonus at low hit points. `is_monster_faster` itself is left alone, because it
also sets the Elbereth engraving weight and the earlier note above records that
retreat behaviour for fast monsters was already measured as neutral (melee is
still worth 16).

This repeats no listed action: it does not cast force bolt (before level 10, off
the first floor, at an adjacent monster, or with less energy), and it does not
change prayer, corpse reach, the food latch, the hunger thresholds, the melee
bonus of the *named* fast monsters, or the zap/ranged heuristics. It only stops a
monster that is genuinely faster than the wizard from being treated as one the
wizard can outrun.

Change the bot from the proposal above. The judge measures that tree.
