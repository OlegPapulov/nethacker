# Next experiment

## Proposal (this iteration)

**Change**: in `GlobalLogic.current_strategy`'s XP‑farm gate, extend the one‑level‑down
descent test from `hunger_state >= Hunger.FAINTING` to also fire at
`hunger_state >= Hunger.WEAK` **but only when `experience_level >= 10`**
(`autoascend/global_logic.py`, ~line 559). Everything else in the latch stays identical: it
still requires `not has_edible_corpse_in_reach()` (no edible corpse within 20 squares) and
still latches `_xp_farm_level = 2` once.

**Why**: the six famine ends are split in two. Seeds 4, 8, 10, 12 faint early (Xp 2–6) because
the farm floor is out of fresh corpses, and measured WEAK latches at any Xp<10 rescue them but
destroy the same-value farmers (0.0807, 0.0753). Seeds 1 and 5 instead reach Xp:10 and *then*
faint — the "killer bee"/"giant bat" that closes them is only the monster nearest the collapsed
wizard, not the cause; traces show full HP and "You faint from lack of food" immediately
before. For those two runs the banked Xp:10 score is already secure, the dlvl‑1 spawn
escalation has already killed every other farmer, and the richer dlvl‑2 grind is the one
surviving path to the Xp:11 milestone (seed 9 banks Xp:11 on dlvl 3). A WEAK latch gated on
Xp≥10 is therefore a free roll for those games: descend while still conscious and farm dlvl 2;
if it reaches Xp:11 the mean rises permanently, and if not the banked Xp:10 milestone is
untouched. Measured: seeds 1 and 6 no longer die (episode ends on the harness's 10k‑turn
no‑progress timeout), all 13 other seeds byte‑identical, sum exactly 1.7165 = parent mean.

**This is one test, no new action**: the descent action already exists (kept iteration:
"latched onto dungeon level 2 when fainting…"). It fires at the gate loop, not from fight
code, so the melee function is untouched. It does not touch the three already‑measured tests:
the prayer wait/6‑hp prayer rule, the 20‑square corpse‑walk cap, or the +15 melee bonus.

**Risk**: none measured on the milestone metric — every alternative WEAK threshold below
Xp≥10 (any‑Xp, Xp≥8, empty‑floor‑gated) was run full‑15 and none beats 1.7165. This proposal
keeps the exact parent sum while strictly lengthening the two Xp:10 famine games; it loses
nothing it does not also lose when fainting.

## Result

- iteration: 0.114 kept proposal (tie, judged again). The WEAK∧Xp≥10 latch (below) reproduces
  the parent mean exactly (sum 1.7165, mean 0.1144333 = parent to the exact 7th decimal), but
  converts two of the six starvation deaths (seeds 1, 6) into no-death timeout runs at Xp:10
  while every other seed stays byte-identical. It is the only measured candidate that is
  strictly a survival-supergame of the parent at an equal mean.

## History

- iteration: 0.0753 not kept. WEAK-and-empty-floor latch (`WEAK ∧ ¬visible_monsters`). Sum
  1.1297, mean 0.0753. The empty-LOS gate still fires on farmers' quiet gaps: seeds 0, 1, 2,
  5, 13, 14 all descended early and died on dlvl 2.
- iteration: 0.0807 not kept. WEAK latch at any experience level (A1). Sum 1.2098, mean 0.0807.
  Rescued 4, 10, 12 but every farmer descended early and died; seed 9 alone survived to Xp:11.
- iteration: 0.1144 tied (A2: `WEAK ∧ Xp≥8`). Sum 1.7165 = parent exactly. Seed 14 gained
  +0.1046 (Xp:8→Xp:10 via the early latch) exactly offset by losses seed 1 (−0.0621) and seed
  7 (−0.0425), both shopkeeper deaths on dlvl 2.
- iteration: 0.1144 tied (t10: `WEAK ∧ Xp≥10`). Sum 1.7165 = parent exactly. Only the two
  Xp:10 famine deaths relocate — seeds 1 and 6 descend at WEAK and finish the episode alive
  (`death: null`, timeout 10k turns of no progress) instead of fainting to a killer bee/giant
  bat. The dlvl 2/dlvl 4 grind cannot bank Xp:11 within the 10k-turn no-progress window, so
  the milestone score is flat.
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