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

## Last iteration

The kept tree scores 0.114 on the 15 `wiz-hum-cha-mal` seeds. That tree waited
for experience level 12 before leaving the first Doom level; it must not be
resubmitted unchanged.

## Why it stopped

All 15 parent games ended in death; mean progress 0.114. No game hit a turn
limit. Nine games never left the first Doom level, and most died in the
Xp:8-Xp:11 band, one or two levels short of the level-12 gate that would let
the wizard descend. See `experience.md` for the per-seed table.

## What is the problem

The wizard has few hit points and little melee damage, so a straight hit-point
exchange with a fast or hard-hitting monster kills it. Eight of fifteen deaths
are exactly that trade: killer bee, giant bat, vampire bat, plains centaur, pony,
kitten, dwarf lord, and Mordor orc (a goblin and a kobold lord do the same at
low levels). The rest are poison (orcish arrow x2) and traps (bolt of fire, bolt
of cold), which are ranged or environmental, not melee.

The bot walks into the melee fights deliberately. `draw_monster_priority_positive`
draws a `+3` approach ring around every non-weak monster, `goto_action` gives
`go_to` a priority of `1`, and melee scores about `16` once the bot is adjacent.
So the bot closes to striking range, then always swaps the last hit instead of
running: melee outbids every flee ring. Earlier experiments only raised the flee
and Elbereth thresholds and could not help for that reason.

## What might solve it

Do not start a melee the hero cannot survive. Add `is_out_trading_us(agent,
monster)` in `autoascend/combat/monster_utils.py`: a monster of difficulty `d`
takes on the order of `d` rounds to put down and hits for on the order of `d` per
round, so exchanging blows costs roughly `2 * d * d` hit points, doubled when the
monster moves faster than we do. If that expected cost exceeds the hit points we
actually have, the trade is unwinnable. Weak monsters and the slow-only-ranged
ones are never out-trading (so XP farming is unchanged), and an unresolved or
invisible monster is assumed out-trading because it cannot be planned.

In `draw_monster_priority_positive` (`autoascend/combat/movement_priority.py`),
for an out-trading monster draw a keep-away gradient (`_draw_away`: priority
grows with Chebyshev distance, `+5` per ring out to 5) and return early, instead
of the normal approach ring. Moving away then outranks the `+3` approach and
beats the `1`-priority `go_to`, and the differing neighbouring priorities make
`goto_action` decline, so the bot breaks contact rather than charging in. Already
adjacent is unchanged: melee still scores 16 there, so a cornered hero fights
instead of freezing. This scales with the hero's own health pool, so a tanky
character still fights most monsters and only a fragile one avoids them; it is
not tied to the wizard.
