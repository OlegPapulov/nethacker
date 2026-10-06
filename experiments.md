# Next experiment

Change one test that already exists: the emergency-prayer cool-down in
`Agent.is_safe_to_pray`.

The only unconditional self-heal the bot has is prayer, gated by
`is_safe_to_pray(500)` for the critically-low-HP prayer and `is_safe_to_pray(400)`
for the fainting prayer. In NetHack 3.6.6 a prayer is answered while in *big
trouble* only if `u.ublesscnt <= 200` (`src/pray.c:can_pray`). Both gates ask for
big trouble - `critically_low_hp` (`hp <= 5 || hp*divisor <= maxhp`, divisor 5 at
level 1-5 and 6 at level 6-13) and `u.uhs >= WEAK` (TROUBLE_STARVING). When the
test fails the prayer is `p_type == 0` ("too soon") and `prayer_done` runs
`change_luck(-3)` and `gods_upset` -> `angrygods`, which is a 1-in-3 `losexp`
(WIS -1, lose one experience level). After that `u.ugangr > 0`, so every later
prayer is `p_type == 1` ("too naughty") and is punished again - the luck loss and
anger are effectively permanent (only a sacrifice on a coaligned altar clears
`u.ugangr`, and chaotic altars are rare here).

`pleased()` sets `u.ublesscnt = rnz(350)`. `rnz` (`src/rnd.c`) is not "about 350":
it is a wide log-scale draw over roughly 35..3498 whose median is a few hundred
and which lands above 700 about half the time. So a 500-turn wait leaves a large,
random fraction of prayers "too soon": they give *no* heal and permanently poison
the bot's relationship with its god. The bot then spends the rest of a 50k-turn
game unable to heal and with negative luck.

Fix: raise the cool-down from 500/400 to 3500 turns. 3500 is the smallest value
that is always past `rnz(350)`'s maximum (3498) plus the 200-turn grace, so any
prayer that passes the gate is guaranteed `p_type == 3` and is a full answer
(the real heal) with no luck loss and no anger. The first prayer is unaffected:
`u.ublesscnt` starts at 300 and drains one point per turn, so the existing
`time > 300` first-prayer branch is already safe.

This changes only the one existing time test (and uses the same value at its
three call sites); it adds no action. The protected seeds (1, 3, 5, 6, 13 at
0.179 and 9 at 0.255) keep their healing and lose only the "too soon" attempts,
which currently deliver no heal and only harm, so they should not fall.

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

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Change one test that already exists. A seed at 0.179 or above must stay there or go higher. A rise on a lower seed does not pay for a fall on a higher seed. Do not add a new action. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
