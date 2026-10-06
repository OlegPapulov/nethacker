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

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Change one test that already exists. The 15 seeds must leave the parent line. A test these games never reach does not change the mean. Do not add a new action. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

## Proposed change

One test, in `autoascend/combat/fight_heur.py`, function `melee_monster_priority`, line 18:

    if agent.blstats.hitpoints > 8 or is_monster_faster(agent, monster):

becomes

    if agent.blstats.hitpoints > max(8, agent.blstats.max_hitpoints // 2) or is_monster_faster(agent, monster):

That test is what decides whether melee is worth 16 or worth 1. Worth 16: melee beats every move the heatmap can offer one-on-one (the strongest retreat is about +12), so the wizard stands beside the monster and trades blows until one of them falls; healing only interrupts below a third of the maximum, and only with an identified potion in the pack. Worth 1: the retreat ring wins, the wizard steps back, regenerates, and re-engages above half. All fifteen games end in combat and seven of them (games 0, 2, 3, 6, 9, 13, 14, Xp:8–11, 0.075–0.255 each) end beside an ordinary monster or its missiles while the wizard is well above 8 hit points and still willing to stand there. The test is reached constantly on these seeds — the wizard fights on depth 1–3 for tens of thousands of turns — so it can move the mean.

The floor keeps the parent exactly: `max_hitpoints <= 16` makes `max(8, max_hitpoints // 2)` equal `8`, so the earliest levels (games 4, 10, 12) play bit-for-bit as before, and `max(8, ...)` is never below `8`, so this only ever removes the +15 — it is a strict subset of the parent's engagements, never a new one. The `or is_monster_faster(...)` side is untouched: a genuinely faster monster (killer bee, giant bat, vampire bat, kitten, pony — games 1, 5, 7, 10, 11) is still fought wherever we stand, because running from a faster monster means taking free hits while we move. Nothing else changes: no new action, no other test, no ring, no gate, no threshold.

Change the bot from the proposal above. The judge measures that tree.
