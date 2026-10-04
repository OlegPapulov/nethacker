# Mutator runs

## Run wiz-hum-cha-mal, 10-minute cap, 3 iterations

The parent batch mean was 0.062. Nine of 15 games end at depth 1. One official death is starvation (seed 13). The written experiment told the agent the usual stop was "killed by a wolf" (2 games) and to change melee.

### Why it stopped

All three iterations exited 137. That is the 10-minute `docker kill`. The agent was still in tool calls or reasoning. No edit was scored (`dev_fitness` empty). The log recorded each iteration twice.

### What is the problem

The cap is doing what it was set to do, and the prompt spends that window re-playing seeds the notes already list. On the last iteration the model had found seed 3 fainting from lack of food and seed 13 starving, and it was about to write its own eval harness when it was killed.

### What might solve it

The notes must forbid another arena run, and a starvation or fainting death must become the experiment even when a monster name is more common. The run log must keep a short reason, not the model's transcript.

## Run 36861664309, wiz-hum-cha-mal, 10-minute cap, 3 iterations

[36861664309](https://github.com/OlegPapulov/nethacker/actions/runs/36861664309) finished with the job green and `0/3` elites. Cold-start mean was 0.062 (the table printed 0.063). Nine of 15 games end at depth 1. The modal death is a wolf (seeds 4 and 11). Seed 13 dies of starvation at 5,206 turns on depth 1. Seed 3 dies to a grid bug at 3,052 turns.

The seed notes already said to eat before exploring and not to re-play the seeds. The agent never rewrote them (`notes_ignored` true).

### Why it stopped

Each coding container was killed at the 10-minute cap. Wall times inside `evolve`: iteration 1 at 819s (~601s of thinking), iteration 2 at 1436s (~615s), iteration 3 at 2052s (~614s). Exit 137, then `aborting — 3 consecutive operator failures`. `dev_fitness` is empty on all three. The only event left in the Actions log is an OpenCode `step_start`. No tool result, no diff, no score.

### What is the problem

The default reasoning variant of `opencode/big-pickle` does not finish one edit inside 10 minutes. The Actions log no longer shows a diagnosis transcript, because the kill lands before a step completes. A longer transcript would not help: the iteration is discarded either way.

### What might solve it

Pass `--effort medium` (OpenCode applies that as `--variant medium` on the pinned model) and kill the container at 20 minutes. The bot experiment stays "eat before exploring."

## Run 36867649207, wiz-hum-cha-mal, 20-minute cap, `--effort medium`

[36867649207](https://github.com/OlegPapulov/nethacker/actions/runs/36867649207) finished green with `0/3` elites. Cold-start mean was 0.062. The published log records three operator errors and no `dev_fitness`.

| Iteration | Thinking time | Last event | Measured |
|---|---|---|---|
| 1 | ~1209s | `step_start`, exit 137 | no |
| 2 | ~1216s | `step_start`, exit 137 | no |
| 3 | ~1216s | `step_start`, exit 137 | no |

`evolve` then aborted on 3 consecutive operator failures.

### Why it stopped

The 20-minute `docker kill` is exit 137. In `nethackers` that path records `operator-error` and never calls the judge. A file the agent wrote inside the container is not a measured bot. The Actions log for this run does not contain a scored iteration.

### What is the problem

The seed header told the agent not to run the arena, and that an unchanged note file discards the edit. The harness brief says the opposite: edit `autoascend/` with a `# hypothesis:` comment, and the judge re-scores the tree after the process exits. Killing the process skips that measurement. Raising the cap from 10 minutes to 20 did not produce a score.

### What might solve it

Stop killing the coding container. Point the seed notes at `experiments.md` and tell the agent to edit `autoascend/` and exit, so the judge can measure the tree.

## Run 36881136099, wiz-hum-cha-mal, no host kill

[36881136099](https://github.com/OlegPapulov/nethacker/actions/runs/36881136099) played all three iterations and the job exited 1. Cold-start mean was 0.063. Each child beat its parent on the 15 public seeds. None of them were published.

| Iteration | Operator | Tokens | Judge mean | Hub |
|---|---|---|---|---|
| 1 | 96 min, completed | 703557 | 0.078 | local-only |
| 2 | 78 min, completed | 679463 | 0.079 | local-only |
| 3 | 85 min, completed | 618055 | 0.081 | local-only |

The judge table for iteration 3 prints 0.082. Seed 13, the starvation game, went from 5,206 turns at depth 1 to 24,520 turns at depth 4. The notes were not rewritten (`notes_ignored` true). The code change was scored anyway.

### Why it stopped

`nethackers` reported `local-only: not published (no gh publisher / dev owner)` on every iteration. `mutator/loop.py` returns 1 when that field is set, so the Actions step is red. The log line `✓ improved 1 cell(s) dev=0.081 (kept local)` is the same fact: the tree beat the parent and stayed on the runner.

### What is the problem

`gh` was logged in. The preflight `GET /user` and the push check both passed. Publish then clones `OlegPapulov/nethacker` into a fresh temp directory and commits there. The job sets `user.name` and `user.email` only on the checkout, so that clone has no author. `git commit` fails, `nethackers` swallows the error, and the hub never sees the tree. The runner is deleted with the 0.081 bot still only in that workspace. The next checkout of `main` is the 0.062 baseline again.

### What might solve it

Set the git author globally in the mutate job, so the publish clone can commit and push. Commit the improved bot from the runner workspace onto `main` as well, so the next run starts from the scored tree if the hub push fails.

## Run 36921712685, wiz-hum-cha-mal, 1 iteration

[36921712685](https://github.com/OlegPapulov/nethacker/actions/runs/36921712685) finished green. Cold-start mean 0.063. One iteration, 78 minutes, 402,750 tokens, then `✓ REGISTERED dev=0.064`. `hub_reason` is empty. The published tree is `ea143fc` on `evo-harness-v1/20261001-203217`.

The edit is the starvation experiment. When hunger reaches weak, the wizard walks to a corpse and eats it. A corpse it is already standing on is treated as fresh. Seed 13 went from starvation at 5,206 turns on depth 1 to 31,848 turns on depth 3 (0.024 to 0.075). Seed 4 went the other way: 32,346 turns on depth 7 (0.179) down to 2,644 turns on depth 1 (0.018). Seed 11 fell from 0.117 to 0.037. The mean moved from 0.063 to 0.064.

### Why it stopped

The job succeeded. The record commit on `main` (`3d6aba1`) contains only `experience.md` and `experiments.md`. The next checkout is still the 0.062 baseline.

### What is the problem

`nethackers` writes the iteration at `runs/<id>/work/iter-0`. `mutator/loop.py` looked for `runs/<id>/iter-0`, found nothing, and did not copy the tree into the checkout. `notes_ignored` is true for the same reason. The hub has the bot. `main` does not.

### What might solve it

Look for `runs/*/work/iter-*`, and copy those two AutoAscend files from `ea143fc` onto `main` so the next seed is the registered bot.

The hub program is `prog_6f3a5ba98505db8d0c2cfd7b9a4f167e`. Its identity list is the one public row at 0.064. There is no verified row, so Private Dungeons has not scored it. This login cannot read `/verify/candidates` (401). Their verifier is the only process that writes that board.

## Run 36934535247, wiz-hum-cha-mal, 2 iterations from the 0.064 parent

[36934535247](https://github.com/OlegPapulov/nethacker/actions/runs/36934535247) finished green with no new elite. Cold start was the 0.064 corpse-eating parent. Seed 14 of that parent still starves (7,795 turns, depth 1). Seed 4 is already the cheap game: 2,644 turns, depth 1, 0.018.

| Iteration | Operator | Judge | Kept |
|---|---|---|---|
| 1 | 140 min, 1,309,209 tokens | 0.063 | no |
| 2 | 17 min, 102,077 tokens | 0.060 | no |

Iteration 1 moved the same eat-when-weak block to the front of `global_strategy` and duplicated sacrificial-corpse pickup (`6b693e2`). Iteration 2 left the block where it was and changed the threshold from weak to hungry (`c66a3d3`).

### Why it stopped

A child is kept only when its mean is strictly above the parent. 0.063 and 0.060 are both below 0.064. The job is green because both scores were published with an empty `hub_reason`. `main` stays on the parent.

### What is the problem

The mean is a few deep games minus a few depth-1 games. Walking to a corpse earlier saves a starvation and spends the turns those deep games used to descend. The parent already does this at weak hunger. Doing it at the front of the strategy list, or at merely hungry, spends more of those turns. The table rounds 0.0635 to 0.064, which hides the miss.

The next parent for an identity has to be this owner's best public commit for that identity. An identity with no public row starts from the AutoAscend import, `8387c34`.

### What might solve it

Seed each identity from that commit before evolve. Tell the agent to leave the weak-hunger threshold alone.

## Run 36951341311, wiz-hum-cha-mal, 2 iterations from the 0.064 parent

[36951341311](https://github.com/OlegPapulov/nethacker/actions/runs/36951341311) finished green with no new elite. The seed was this owner's best public bot for the identity. Cold-start mean was 0.06431333032572426, the same number as that parent. Seed 14 of the parent still starves (7,795 turns, depth 1). Six of 15 games end at depth 1. The note named the modal death, a jackal (seeds 9 and 11), and told the agent to leave the weak-hunger threshold and change one other decision.

| Iteration | Operator | Judge | Kept | Commit |
|---|---|---|---|---|
| 1 | 166 min, 4,953,018 tokens | 0.06431333032572426 | no | `47e65cb` |
| 2 | 72 min, 969,128 tokens | 0.062584 | no | `9917b47` |

Iteration 1 added a distance cap inside `eat_corpses_from_ground`: when hunger is below weak and the walk is non-local, keep only corpses within 3 squares. That branch cannot run. A non-local walk is already called only when hunger is at least weak. The 15 public seeds replayed the parent. The printed mean is 0.064 because the table rounds.

Iteration 2 removed that cap and edited five combat decisions plus inventory eating (`9917b47`). Melee priority now wants more than 12 hit points instead of 8. Elbereth engraves below 40 hit points instead of 30. `imminent_death_on_melee` flees at 12 hit points, or 20 against a dangerous monster, instead of 8 and 16. The flee radii got larger. `eat_from_inventory` will eat any corpse `_is_corpse_editable` accepts, not only lizard and lichen. It also changed `mon in WEAK_MONSTERS` to `mon.mname in WEAK_MONSTERS`. `WEAK_MONSTERS` is a list of names, so the old check was always false.

| Seed | Parent | Iteration 2 |
|---|---|---|
| 6 | 0.117, depth 5, 27,730 turns, lynx | 0.000, depth 1, 1,289 turns |
| 2 | 0.075, depth 5 | 0.037, depth 1 |
| 7 | 0.117, depth 5 | 0.075, depth 5 |
| 1 | 0.117, depth 3 | 0.075, depth 3 |
| 4 | 0.018, depth 1, 2,644 turns | 0.075, depth 5 |
| 8 | 0.021, depth 1 | 0.075, depth 4 |
| 11 | 0.037, depth 1 | 0.117, depth 4 |
| 12 | 0.024, depth 1 | 0.075, depth 3 |
| 13 | 0.075, depth 3 | 0.117, depth 5 |
| 14 | 0.029, depth 1, starvation | 0.051, depth 1 |

### Why it stopped

A child is kept only when its mean is strictly above the parent. Iteration 1 tied the parent on every seed. Iteration 2 scored 0.063. Both `hub_reason` values are empty, so the job is green. `main` stays on the 0.064 parent.

### What is the problem

The mean is the long games. Fleeing earlier saved several depth-1 deaths and shortened the games that were already deep. Seed 6, a 0.117 game, became a zero. "Change one other decision" was read as a license to retune every combat threshold in one diff.

The first edit spent 166 minutes and 4.9 million tokens on a branch the hunger gate makes unreachable. The playthrough header still calls a jackal the usual stop, because that string appears twice, while the starvation game is the one the hypothesis was written for.

### What might solve it

Name one function in the note. Tell the agent not to edit `eat_corpses_from_ground`, because a distance cap there never runs. The one allowed edit is `imminent_death_on_melee`: raise the ordinary cut from 8 hit points to 10, and leave the dangerous-monster cut at 16. Leave Elbereth, melee priority, flee radii, and `eat_from_inventory` alone.

## Run 36983992379, wiz-hum-cha-mal, 2 iterations, no code change

[36983992379](https://github.com/OlegPapulov/nethacker/actions/runs/36983992379) finished green with no new elite. Cold-start mean was 0.06431333032572426. Both children scored that same number, and every seed in both judge tables matches the parent turn for turn.

| Iteration | Operator | Judge | Code |
|---|---|---|---|
| 1 | 154 min, 943,879 tokens | 0.06431333032572426 | identical to the seed, `d779a91` |
| 2 | 178 min, 686,407 tokens | 0.06431333032572426 | identical to iteration 1 except `experiments.md`, `2aec99d` |

`autoascend/` in `d779a91` matches the seeded commit `47e65cb`. Iteration 2 adds 44 lines to `experiments.md` and no Python. The note says the agent tried the 8-hit-point cut, a search-budget change, and earlier corpse eating in a private `peval.py`, then put the parent back. Those numbers are not judge scores.

### Why it stopped

A child is kept only when its mean is strictly above the parent. Both means are the parent, because the judged files are the parent. `hub_reason` is empty. `main` stays on the 0.064 bot.

### What is the problem

The operator brief tells the model to measure a sample itself, and that a change which only matches the parent is discarded. The seed note asked for an 8-to-10 hit-point tweak and told it not to run the arena. The model followed the brief: it spent both iterations measuring, decided the tweak was not worth keeping, and restored the parent so the judge would not see a loser. The judge then scored the parent twice.

There is no lost edit in the loop. The publish contains the tree the operator left behind, and that tree has no Python diff.

`parse_spellcast_view` returns immediately unless the role is a healer, so a wizard's `known_spells` stays empty. The healing casts in `emergency_strategy` are commented out. The wizard never casts. That is a different change from another hit-point cut.

### What might solve it

Tell the agent to leave the edit in the tree. A local game is not the score, and restoring the parent makes the judge score the parent. The edit is the wizard spell path: parse the spell menu for a wizard, and cast `force bolt` from `emergency_strategy` when it is known, energy is at least 5, and a monster is adjacent.

## Run 37023219996, wiz-hum-cha-mal, 2 iterations, 0.077 kept

[37023219996](https://github.com/OlegPapulov/nethacker/actions/runs/37023219996) finished green. Cold start was 0.06431333032572426. Iteration 1 registered 0.07737020128671113 (`fb8c262`). Iteration 2 scored that same number, and its judge table matches iteration 1 on every seed. One new elite.

| Seed | Parent | Iteration 1 |
|---|---|---|
| 13 | 0.075, depth 3, 31,848 turns | 0.179, depth 6, 36,762 turns |
| 14 | 0.029, depth 1, 7,795 turns, starvation | 0.117, depth 3, 28,988 turns |
| 5 | 0.037, depth 1, 8,788 turns | 0.117, depth 2, 29,992 turns |
| 6 | 0.117, depth 5 | 0.075, depth 4 |
| 7 | 0.117, depth 5 | 0.075, depth 3 |
| 10 | 0.075, depth 4 | 0.024, depth 1 |

### Why it stopped

Iteration 1 is strictly above the parent, so it was kept. Iteration 2 ties that child, so it was not kept. `hub_reason` is empty. The record commit on `main` (`f4316da`) contains only the two markdown files.

### What is the problem

The improved tree was copied into `.mutator-run/parent`, the directory the loop pulled, and not into the checkout. The record step commits the checkout, so `main` stayed on the 0.064 bot.

The live change in `fb8c262` is a cap of 20 squares on a corpse walk once hunger is weak. The parent walked any distance. Seed 14, the starvation game, went from depth 1 to depth 3.

The force bolt block does not run. Both calls to `parse_spellcast_view` are still commented out. The wizard branch that writes `force bolt` into `known_spells` is inside that function. `_parse` now sets `known_spells` to an empty dict whenever the character is read. The published tree also adds `autoascend/agent.py.test`, a second copy of `agent.py`, which nothing imports.

### What might solve it

Copy a kept tree onto the checkout as well as the pull directory. The next note leaves the 20-square cap alone and tells the agent to call `parse_spellcast_view` once the role is known, and to stop clearing `known_spells` inside `_parse`.

## Run 37077364014, wiz-hum-cha-mal, 2 iterations, no new elite

[37077364014](https://github.com/OlegPapulov/nethacker/actions/runs/37077364014) finished green. Parent mean 0.07737020128671113. Both children scored that same number. Every judge seed matches the parent turn for turn. No new elite.

| Iteration | Operator | Code |
|---|---|---|
| 1 | ~86 min, 570,147 tokens | no Python change, `78c6c67` |
| 2 | ~73 min, 705,600 tokens | spell parser and a deleted cast, `a27b54a` |

The 0.077 parent still has five depth-1 games: seed 4 dies to a kobold zombie at 2,644 turns, seed 12 to a bat at 4,917, seed 10 to a coyote at 6,746, seed 11 to a bat at 9,791, seed 8 to a newt at 9,957. No game starves.

### Why it stopped

A child is kept only when its mean is strictly above 0.077. Both means are 0.077. `main` stays on that bot.

### What is the problem

Iteration 1 never edited `autoascend/`. Iteration 2 called `parse_spellcast_view` at startup and stopped clearing `known_spells`, then removed the only `self.cast('force bolt', ...)` from `emergency_strategy`. The spell list is filled and nothing casts. Opening the menu and pressing escape does not take a turn, so the 15 games are the parent. The smoke seed moved by 6 turns, so the judge did run the new code.

### What might solve it

The next note asks for a cast that stays in the file. Cast force bolt only when energy is at least 5 and an adjacent monster would make `imminent_death_on_melee` true, and that monster is not a pet and not in `WEAK_MONSTERS`. Do not cast at every adjacent glyph. Leave the 20-square corpse cap alone.

## Run 37110207188, wiz-hum-cha-mal, 1 iteration, identical tree

[37110207188](https://github.com/OlegPapulov/nethacker/actions/runs/37110207188) finished green. The operator ran about 70 minutes and used 425,200 tokens. The gate then said `child identical to parent`. `dev_fitness` is empty. `autoascend/` did not change, and the notes did not change. No published commit. The parent stays at 0.077.

### Why it stopped

The gate hashes the solution and refuses to call the judge when the hash matches the parent. An identical tree is not a score of 0.077. It is no score.

### What is the problem

The bot was not rewritten. Three instructions disagree about what finishing means. The seed header says leave a `self.cast` and do not restore the parent. `mutator/GAME_RULES.md` said the job is done when `experience.md` and `experiments.md` are rewritten. The operator brief, which this repo does not write, says to measure a sample and that a tree matching the parent is discarded. The operator left the parent in place. The notes were not rewritten either, so the game-rules line was not what it followed.

The note is also frozen for the whole `evolve` call. A later iteration is not told that the previous tree was identical and was thrown away.

### What might solve it

Say the same thing in the header and in `GAME_RULES.md`: the edit is an action in `autoascend/`, and an identical tree is not scored. Run one iteration at a time, and put the previous tree's result at the top of the next note. The survival edit is the fatal melee on depth 1: cast force bolt when `imminent_death_on_melee` is true for a hostile monster that is not weak, and otherwise step toward a door or a corridor.

## Run 37115352184, wiz-hum-cha-mal, 1 iteration, same 15 games

[37115352184](https://github.com/OlegPapulov/nethacker/actions/runs/37115352184) finished green. The operator ran about 114 minutes and used 599,843 tokens. The judge scored 0.07737020128671113, the parent number. Every one of the 15 seeds matches the parent turn for turn. Not kept. `main` stays on the 0.077 bot.

`70fae4d` is the same `autoascend/` as `a27b54a`, the spell-menu tree from the run before. It calls `parse_spellcast_view` at startup and has no `self.cast('force bolt')`. The smoke seed is 1,899 turns, the same smoke as that earlier tree. `code_unchanged` is false only because that tree differs from the 0.077 parent. The games do not.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is the parent.

### What is the problem

The note asked for a cast and a step away from a fatal melee. The operator submitted the spell parser again. That parser does not take a turn, so the judge replays the parent. Asking for a cast in `emergency_strategy` keeps producing this diff, because the cast gets deleted and the parser remains.

In `draw_monster_priority_negative`, a fast monster that is already adjacent hits `pass`. A bat is fast. Seeds 11 and 12 die to a bat on depth 1. The bot does not step off that square.

### What might solve it

Name that one function and forbid `character.py`. When `imminent_death_on_melee` is true, draw the same negative ring for a fast adjacent monster that the code already draws for a slow one. Do not leave the `pass`.

## Run 37123137695, wiz-hum-cha-mal, 1 iteration, ring does not beat melee

[37123137695](https://github.com/OlegPapulov/nethacker/actions/runs/37123137695) finished green. The operator ran about 143 minutes. The judge scored 0.07737020128671113. Progress and turn count match the parent on every seed. Not kept. `main` stays on the 0.077 bot. Published as `4e9d706`.

The named function did change. In `draw_monster_priority_negative`, a fast adjacent monster now draws -5 at radius 1 and -10 at radius 2. The same tree also rewrites the spell parser, `cast`, inventory wear, and adds `agent.py.test`.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is the parent.

### What is the problem

`fight2` takes the action with the highest priority. `melee_monster_priority` returns 16 for a faster monster, because it adds 15 whenever hit points are above 8 or the monster is faster. A bat is faster, so the swing stays at 16 even at 1 hit point. After the ring is subtracted from the square the bot is standing on, a step away is worth about 5 to 10. The swing still wins, so the 15 games do not move.

### What might solve it

Leave the heatmap alone. In `melee_monster_priority`, when `imminent_death_on_melee` is true and the monster is faster, do not add 15. The swing has to rank below a step onto an adjacent walkable square.

## Run 37133701364, wiz-hum-cha-mal, 1 iteration, search cut

[37133701364](https://github.com/OlegPapulov/nethacker/actions/runs/37133701364) finished green. The operator ran about 178 minutes. The judge scored 0.04036337256709107. The parent is 0.07737020128671113. Not kept. `main` stays on the 0.077 bot. Published as `54245b6`.

The operator did not edit `melee_monster_priority`. The new code prefers unseen tiles over a search in `exploration_logic.py`. Against the previous ring tree, that file is the only change. The notes were not rewritten.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What is the problem

Seeds 10 and 12, the coyote and one bat, went from 0.024 to 0.075. Seed 13 went from 0.179 to 0.024. Seeds 0, 5, 9, and 14 also fell. The task paragraph did not forbid `exploration_logic.py`. The playthrough note said that a longer long game raises the mean.

The melee line in the task does not match the five short games. A coyote, a kobold zombie, and a newt get the extra 15 only while hit points are above 8. `imminent_death_on_melee` is true for them only at 8 or below, and by then the 15 is already absent. A soldier ant is an insect, so that check is true at 16 hit points. The same line would change the long insect fights and would not change three of the five short games.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37145731075, wiz-hum-cha-mal, 1 iteration, food latch kept

[37145731075](https://github.com/OlegPapulov/nethacker/actions/runs/37145731075) finished green. The job ran about 214 minutes. The judge scored 0.08021001539051657. The parent is 0.07737020128671113. The child was kept. `main` has this bot in `85f7c2a`.

The operator did not edit `melee_monster_priority`. The new behavior latches `_xp_farm_level` to dungeon level 2 when hunger is fainting and no edible corpse is within 20 squares. The tree also has the spell parser and the negative ring.

### Why it stopped

A child is kept when its mean is strictly above the parent. This mean is higher.

### What is the problem

Ten seeds have the same turn count as the parent. Seed 11 went from 0.037 to 0.075. Seed 9 went from 0.117 to 0.179. Seed 13 went from 0.179 to 0.117. Seeds 4, 8, and 10 stayed at the same progress. The melee edit is still absent.

### What might solve it

Leave the latch in place. The next edit is still `melee_monster_priority` on depth 1 for a monster that is not in `INSECTS`. The operator writes the comment and the experiment line in ASD-STE100 style.

## Run 37159253981, wiz-hum-cha-mal, 1 iteration, experience gate 12

[37159253981](https://github.com/OlegPapulov/nethacker/actions/runs/37159253981) finished green. The job ran about 171 minutes. The judge scored 0.11444300565928403. The parent is 0.08021001539051657. The child was kept. `main` has this bot in `0159367`.

The operator did not edit `melee_monster_priority`. The parent leaves the first Doom level at experience level 8. The child waits until experience level 12. The notes were not rewritten.

### Why it stopped

A child is kept when its mean is strictly above the parent. This mean is higher.

### What is the problem

Seeds 0, 1, 3, 5, 6, 7, 9, and 13 rose. Seed 9 went from 0.179 to 0.255. Seeds 4, 8, 10, and 12 kept the same turn count, so the new gate never ran in those games. Seed 14 fell from 0.117 to 0.075. A longer stay on Doom can lower a score. The comment in the child says the opposite.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37169391861, wiz-hum-cha-mal, 2 iterations, cancelled

[37169391861](https://github.com/OlegPapulov/nethacker/actions/runs/37169391861) was cancelled at the six-hour limit. `main` stays on the 0.114 bot.

Iteration 1 scored the parent mean. Every seed matches the parent turn for turn. The child was not kept. The tree is `ba748d8`. The operator used about 700,799 tokens.

The operator did not remove the 15-point bonus. The edit changes the launcher penalty. The parent subtracts 6 when the bot holds a ranged weapon. The child subtracts 6 only when hit points are below half. The 15 games do not move.

Iteration 2 started at 04:24 UTC and had no score when the job stopped at 07:54 UTC.

### Why it stopped

The Actions job stops at 360 minutes. Two operator runs do not finish inside that limit.

### What is the problem

The note said "do not add 15". The operator edited the neighbor line, `ret -= 6`. A wizard rarely holds a ranged weapon, so that line does not run.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37190939148, wiz-hum-cha-mal, 1 iteration, same launcher edit

[37190939148](https://github.com/OlegPapulov/nethacker/actions/runs/37190939148) finished green. The job ran about 82 minutes. The judge scored 0.11444300565928403. The mean turn count is 36,648. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 4,019 seconds and used 355,484 tokens. The tree `323884d` matches `ba748d8`. Both change `ret -= 6`. The `ret += 15` line stays.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is the parent.

### What is the problem

The note says "Do not edit the `ret -= 6` line. That launcher change scored 0.114." The parent score is 0.114. The sentence reads like the launcher edit reaches the current best. The operator submitted that edit again, with the same comment.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37201393031, wiz-hum-cha-mal, 1 iteration, launcher line and prayer wait

[37201393031](https://github.com/OlegPapulov/nethacker/actions/runs/37201393031) finished green. The job ran 70 minutes, from 12:21 UTC to 13:31 UTC. The judge scored 0.11444300565928403. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 3,645 seconds and used 422,458 tokens. The judge ran for 467 seconds. Setup before the operator clock was about 70 seconds. The previous one-iteration job ran 82 minutes.

The tree is `524d774`. It changes `ret -= 6` the same way as `ba748d8`. The `ret += 15` line stays. It also adds a 2,000-turn wait in `agent.py` after the message `Thou art arrogant`. The notes were not rewritten.

Seed 4 went from 2,742 turns to 2,694. Seed 10 went from 6,313 turns to 6,435. Every seed has the same progress as the parent. The mean turn count is 36,653. The parent mean turn count is 36,648.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is the parent.

### What is the problem

The note says "Leave `ret -= 6` unchanged." The operator edits that line. This is the third judged copy of the launcher edit. The header does not forbid `agent.py`, so the operator also adds the prayer wait. The `ret += 15` line stays.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37209219942, wiz-hum-cha-mal, 1 iteration, cancelled

[37209219942](https://github.com/OlegPapulov/nethacker/actions/runs/37209219942) was cancelled at the 360-minute limit. The job ran from 14:25 UTC to 20:26 UTC. There is no child score. `main` stays on `b2f353e`.

The operator finished. The operator used 1,542,509 tokens. The clock at that line is 21,304 seconds. The one-cell cold start took 578 seconds. The judge started the 15-seed batch and did not finish. The smoke seed scored 0.021.

The cold-start table matches `524d774` on every seed. The mean is 0.114. The mean turn count is 36,653. The log does not show the operator diff.

### Why it stopped

The Actions job stops at 360 minutes. The operator used the whole window. The judge had no time left.

### What is the problem

The harness brief tells the operator to play seeds and to wait up to 600000 ms. The seed header says not to play. The log does not show which text the operator followed. The token rate was 74 per second, close to the shorter runs. The count is high because the operator stayed open.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37233060279, wiz-hum-cha-mal, 1 iteration, difficulty gate

[37233060279](https://github.com/OlegPapulov/nethacker/actions/runs/37233060279) finished green. The job ran 33 minutes, from 21:13 UTC to 21:46 UTC. The judge scored 0.08065773574577405. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 1,695 seconds and used 339,606 tokens. The judge ran for 232 seconds. The brief patch step succeeded. The notes were rewritten.

The cold-start table matches `524d774` on every seed. That tree is an unkept 0.114 program. `best_public` keeps the first row when the score ties, because the test is `>`. The checkout is the kept bot. The seed was not the checkout.

The only new lines versus `524d774` are in `melee_monster_priority`. The operator did not copy the depth-1 block. The new test is `getattr(mon, 'difficulty', 21) <= experience_level`. An unseen monster gets 21, so it never gets the bonus.

Seed 8 rose from 0.037 to 0.179. Seed 0 rose from 0.117 to 0.179. Seed 11 rose from 0.075 to 0.117. Seed 9 fell from 0.255 to 0.029, and from 69,906 turns to 3,041. Seeds 1, 3, 5, 6, and 13 fell from 0.179. Seeds 4, 10, and 12 kept the same turn count. The mean turn count is 25,073.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is below the parent.

### What is the problem

The task showed the exact block and also said "do not add 15". The operator wrote a different condition. That condition applies on every depth. Seed 9, the only Xp:11 game, died at Xp:5. The rise on seed 8 does not cover that fall. Three of the four short games did not move.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

