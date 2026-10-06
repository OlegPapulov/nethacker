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

## Run 37238643759, wiz-hum-cha-mal, 2 iterations, two new bonuses

[37238643759](https://github.com/OlegPapulov/nethacker/actions/runs/37238643759) finished green. The job ran from 22:05 UTC to 03:01 UTC. That is 4 hours 57 minutes. Neither child was kept. `main` stays on the 0.114 bot.

Iteration 1 scored 0.07877540225284915. The operator ran for 10,561 seconds and used 827,938 tokens. Iteration 2 scored 0.06537336057393453. The operator ran for 6,359 seconds and used 422,813 tokens. The notes were rewritten both times.

Both cold-start tables have 36,648 mean turns. That is the checkout. The tie rule kept `524d774` out. Iteration 2 also started from the checkout, because iteration 1 was not kept.

The `ret += 15` lines stay in both trees. Both diffs insert code before `return ret`. Iteration 1 adds a bonus from monster difficulty and speed. Iteration 2 adds a bonus from the melee roll and armor class when two monsters stand adjacent.

Seeds 4, 10, and 12 keep 2,742, 6,313, and 5,011 turns in both children. In iteration 1, seed 6 rose from 0.179 to 0.255, seed 7 rose from 0.117 to 0.179, and seed 8 rose from 0.037 to 0.075. Seed 9 fell from 0.255 to 0.029. In iteration 2, seed 2 rose from 0.075 to 0.117. Seed 9 fell from 0.255 to 0.117. Seeds 1, 3, and 13 fell to 0.037.

### Why it stopped

A child is kept only when its mean is strictly above the parent. Both means are below 0.114.

### What is the problem

The task said to copy the second block over the first. The operator wrote a new bonus at the end of the function. A new bonus picks a different target. It does not remove the step into melee. The short games stay short. Seed 9, the only Xp:11 game, fell in both iterations.

The kept gains in this repo came from the corpse cap, the food latch, and the level-12 gate. Those edits left `melee_monster_priority` alone. The recent edits inside that function scored 0.114, 0.081, 0.079, and 0.065.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37286220190, wiz-hum-cha-mal, 1 iteration, Elbereth not uncommented

[37286220190](https://github.com/OlegPapulov/nethacker/actions/runs/37286220190) finished green. The job ran from 08:51 UTC to 11:15 UTC. The judge scored 0.11444300565928403. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 7,953 seconds and used 818,133 tokens. The judge ran for about 10 minutes. The cold-start mean turns are 36,648. The child mean turns are 36,648. The notes were not rewritten.

`autoascend/` matches the parent. The Elbereth block stays commented. The tree adds `nle.ttyrec3.bz2`. `fight_heur.py` was not edited.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is the parent.

### What is the problem

The task said to remove the comment marks in `emergency_strategy`. The operator did not edit that function. The bot then plays the parent games. The score cannot rise.

The commented block is still the wrong next edit if someone uncomments it as written. `emergency_strategy` is the outer preempt, so it runs before `fight2`. The test is hit points below 5, or below one fifth of the maximum. A new wizard meets that test. The engrave takes a turn while the monster is already adjacent. The block then rests for up to 8 turns. A monster that ignores Elbereth hits during those rests. When `can_engrave` is false, the block does not run, and the short games stay short.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37310611617, wiz-hum-cha-mal, 1 iteration, one Elbereth engrave

[37310611617](https://github.com/OlegPapulov/nethacker/actions/runs/37310611617) finished green. The job ran from 12:35 UTC to 13:02 UTC. The judge scored 0.11101507289173372. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 1,174 seconds and used 162,960 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.111 and 35,028 turns. The notes were rewritten.

The only bot change is 18 lines in `emergency_strategy`. The commented rest loop stays commented. The new branch does not call `direction('.')`. `fight_heur.py` was not edited. The tree has no ttyrec.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What is the problem

Seed 4 rose from 0.018 to 0.117. Its turns rose from 2,742 to 29,415. Seed 3 fell from 0.179 to 0.029. Its turns fell from 57,042 to 5,383. The gain on seed 4 is smaller than the loss on seed 3.

The instruction said `blstats.depth` is 1. The operator used `depth <= 3`. The operator also skipped undead, demons, and mindless monsters. Seed 3 died at depth 1.

`emergency_strategy` is the outer preempt, so this branch runs before `fight2`. Prayer and a healing potion run first. When those do not fire, the new branch writes Elbereth with the fingers. `engrave()` takes that turn. The word is on the floor after the turn. The adjacent monster attacks during the turn. A small hit lets the word finish, and later attacks stop. That is seed 4. A killing hit ends a game that used to fight through the same dip. That is seed 3.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37331933484, wiz-hum-cha-mal, 1 iteration, Elbereth with no monster adjacent

[37331933484](https://github.com/OlegPapulov/nethacker/actions/runs/37331933484) finished green. The job ran from 15:19 UTC to 15:48 UTC. The judge scored 0.10213461846666004. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 1,097 seconds and used 115,296 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.102 and 34,637 turns. The notes were not rewritten.

The only bot change is 29 lines in `emergency_strategy`. The condition is depth 1, hit points below 6, `can_engrave()`, the word is not already there, and no monster is adjacent. The rest loop stays commented. The branch does not call `direction('.')`. `fight_heur.py` was not edited.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What is the problem

Seed 4 rose from 0.018 to 0.051. That is Xp:2 to Xp:7. Its turns rose from 2,742 to 19,961. Seed 8 rose from 0.037 to 0.075. That is Xp:6 to Xp:8. Its turns rose from 9,957 to 36,419.

Seed 3 fell from 0.179 to 0.029. That is Xp:10 to Xp:5. Its turns fell from 57,042 to 5,338. Seed 13 fell from 0.179 to 0.075. That is Xp:10 to Xp:8. Its turns fell from 48,694 to 27,349.

After the word is on the floor, `fight_heur.py` subtracts 100 from melee, ranged, and zap. `wait_action` then scores about 30. The bot stands on the word.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37337111283, wiz-hum-cha-mal, 2 iterations, search then retreat

[37337111283](https://github.com/OlegPapulov/nethacker/actions/runs/37337111283) failed after both scores. The hub read timed out on the second register. The job ran from 15:58 UTC to 17:12 UTC. Neither child was kept.

Iteration 1 scored 0.0835879839759868. It searches for up to 25 turns in `emergency_strategy`. Seed 4 rose from 0.018 to 0.029. Seed 9 fell from 0.255 to 0.179.

Iteration 2 scored 0.07432499773456397. It steps away when hit points are at most one third of the maximum. Seed 4 stays at 2,742 turns. Seed 3 fell from 0.179 to 0.021.

## Run 37349624888, wiz-hum-cha-mal, 1 iteration, melee tie-break in fight2

[37349624888](https://github.com/OlegPapulov/nethacker/actions/runs/37349624888) finished green. The job ran from 17:35 UTC to 18:16 UTC. The judge scored 0.09228385325013148. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 1,863 seconds and used 301,610 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.092 and 31,701 turns. The notes were rewritten.

The only bot change is 25 lines in `fight2`. `emergency_strategy` stays as the parent wrote it. When two melee actions share a priority, the bot keeps the last target, and otherwise it prefers a faster or a dangerous monster.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What is the problem

Seed 4 stays at 2,742 turns and 0.018. Seeds 10 and 12 keep their turn counts. Seed 9 fell from 0.255 to 0.179. That is Xp:11 to Xp:10. Seed 1 fell from 0.179 to 0.051. That is Xp:10 to Xp:7. Seed 3 fell from 0.179 to 0.117. That is Xp:10 to Xp:9.

The tie-break runs only when two melee actions have the same priority. Seed 4 never reaches a different action, so its death stays. The long games do reach that tie, and their progress falls.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37355608122, wiz-hum-cha-mal, 1 iteration, latch waits for level 5

[37355608122](https://github.com/OlegPapulov/nethacker/actions/runs/37355608122) finished green. The job ran from 18:23 UTC to 18:47 UTC. The judge scored 0.10209517981729713. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 781 seconds and used 42,794 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.102 and 33,792 turns. The notes were rewritten.

The only bot change is the fainting test in `current_strategy`. It now requires `experience_level >= 5` before it sets `_xp_farm_level` to 2. `experience_level >= 12` stays. `fight2` and `emergency_strategy` stay as the parent wrote them.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What is the problem

Seed 4 stays at 0.018. Its turns go from 2,742 to 2,644, and it dies on depth 1. Seed 12 falls from 0.029 to 0.024. Seed 9 falls from 0.255 to 0.075. That is Xp:11 to Xp:8. Its turns fall from 69,906 to 26,819. That one seed is the mean.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37362877624, wiz-hum-cha-mal, 1 iteration, descend on a dry floor

[37362877624](https://github.com/OlegPapulov/nethacker/actions/runs/37362877624) finished green. The job ran from 19:21 UTC to 20:14 UTC. The judge scored 0.04561779964972383. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 2,387 seconds and used 367,470 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.046 and 18,573 turns. The notes were rewritten.

The only bot change is 60 lines in `current_strategy`. The fainting latch stays. The new branch walks to a down stair when the floor has no visible monster and no edible corpse, down through dungeon level 5. `_deep_farm_level` only increases, so the latch cannot pull the wizard back up. The `experience_level >= 11` line is absent.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What is the problem

Seed 4 stays at 2,742 turns and 0.018. Seed 10 rises from 0.024 to 0.037. Seed 12 rises from 0.029 to 0.037. Seed 2 rises from 0.075 to 0.117. Seed 9 falls from 0.255 to 0.051. Its turns fall from 69,906 to 7,581, and it dies on depth 4. Seed 0 falls from 0.117 to 0.021. Seed 6 falls from 0.179 to 0.029.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37372752441, wiz-hum-cha-mal, 1 iteration, stay on level 1 below level 6

[37372752441](https://github.com/OlegPapulov/nethacker/actions/runs/37372752441) finished green. The job ran from 21:11 UTC to 21:49 UTC. The judge scored 0.10051000771701067. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 1,335 seconds and used 157,546 tokens. The cold-start mean is 0.114. The child mean is 0.101 and 32,880 turns.

The only bot change is 8 lines in `current_strategy`. When `experience_level < 6` and the farm target is below dungeon level 1, the target becomes dungeon level 1.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37383680703, wiz-hum-cha-mal, 1 iteration, cast before fight2

[37383680703](https://github.com/OlegPapulov/nethacker/actions/runs/37383680703) finished green. The judge scored 0.06642128837653834. The table printed 0.067. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 1,409 seconds and used 196,708 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.067 and 22,878 turns.

The operator added `cast_at_monsters` and called it before `fight2`. The spell is an attack spell at distance 2 to 6.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

## Run 37387762326, wiz-hum-cha-mal, 1 iteration, `--effort high`, leave a used-up floor

[37387762326](https://github.com/OlegPapulov/nethacker/actions/runs/37387762326) finished green. The judge scored 0.11444300565928403. The child was not kept. The mean equals the parent.

The operator ran for 3,277 seconds and used 737,660 tokens. The child mean is 36,040 turns. The parent mean is 36,648 turns.

The operator added `_floor_is_used_up` in `global_logic.py`. When that test is true, the farm target becomes the next Doom level, with a cap of 4. The comment says eleven seeds stall on one experience level. Five seeds share the most common parent progress, 0.179. Fourteen seeds keep the parent progress and the parent turn count. Seed 6 changes from 73,840 turns at depth 3 to 64,713 turns at depth 2. Its progress stays 0.179.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is equal.

## Run 37397657802, wiz-hum-cha-mal, 3 iterations, `--effort xhigh`

[37397657802](https://github.com/OlegPapulov/nethacker/actions/runs/37397657802) finished green. The job ran from 01:08 UTC to 03:05 UTC. No child was kept. `main` stays on the 0.114 bot. Each iteration starts from that parent. The cold-start mean is 0.114 and 36,648 turns on every iteration. `notes_ignored` is false on every iteration.

### Iteration 1, gold

The operator ran for 2,577 seconds and used 627,854 tokens. The judge scored 0.053290418490603744. The table printed 0.053. The child mean is 17,394 turns.

The edit is in `ItemPriority`. The parent picks up coins when `_drop_gold_till_turn` is already past. The child picks up coins only while that deadline is still active. The comment says a gold pile fills the weight budget and blocks potions and food.

Seeds 4, 8, and 12 rise. Seed 4 goes from 0.018 to 0.029. Seed 8 goes from 0.037 to 0.075. Seed 12 goes from 0.029 to 0.117. Seed 9 falls from 0.255 to 0.029, and from 69,906 turns to 3,153 turns.

### Iteration 2, Elbereth

The operator ran for 1,252 seconds and used 157,566 tokens. The judge scored 0.09002482586758531. The table printed 0.090. The child mean is 27,240 turns.

`can_engrave` returns false while hit points are below the maximum. The comment says the word makes melee, ranged, and zap lose priority, so the bot stands and takes hits.

Seeds 4, 8, and 12 keep the parent turn counts. Seed 6 rises from 0.179 to 0.255, and from 73,840 turns to 81,023 turns. Seeds 3 and 5 fall from 0.179 to 0.029. Seed 9 falls from 0.255 to 0.179.

### Iteration 3, retreat

The operator ran for 1,905 seconds and used 408,481 tokens. The judge scored 0.07239138816724316. The table printed 0.072. The child mean is 23,376 turns.

`is_out_trading_us` treats `2 * difficulty * difficulty` as the hit-point cost of a melee exchange, and twice that when the monster is faster. When that cost exceeds current hit points, the movement priority walks away.

Seeds 4, 8, and 12 keep the parent turn counts. Seed 11 rises from 0.075 to 0.117. Seed 9 falls from 0.255 to 0.051. Seeds 1 and 3 fall from 0.179 to 0.037.

### Why it stopped

A child is kept only when its mean is strictly above the parent. Each of these means is lower.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37439589596, wiz-hum-cha-mal, 1 iteration, `--effort xhigh`, `can_engrave` returns false

[37439589596](https://github.com/OlegPapulov/nethacker/actions/runs/37439589596) finished green. The job ran from 08:57 UTC to 10:27 UTC. The judge scored 0.09002482586758531. The table printed 0.090. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 4,899 seconds and used 469,390 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.090 and 27,240 turns. `notes_ignored` is false.

`can_engrave` now returns false on every call. The comment quotes the new sentence: a wait under Elbereth ends the fight at the current experience level. The comment also says `fight_heur.py`, `fight2`, and `emergency_strategy` are off limits, so the edit is the gate those functions call.

The 15 seed rows match iteration 2 of run 37397657802. That earlier edit returned false only while hit points were below the maximum. This edit returns false always. The score is the same number.

Seed 6 rises from 0.179 to 0.255, and from 73,840 turns to 81,023 turns. Seeds 3 and 5 fall from 0.179 to 0.029. Seed 9 falls from 0.255 to 0.179. Seeds 4, 8, and 12 keep the parent turn counts.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37450590226, wiz-hum-cha-mal, 1 iteration, `--effort high`, prayer wait of 1,200 turns

[37450590226](https://github.com/OlegPapulov/nethacker/actions/runs/37450590226) finished green. The judge scored 0.04406781738617764. The table printed 0.044. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 6,702 seconds and used 958,790 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.044 and 11,366 turns. `notes_ignored` is false.

`is_safe_to_pray` now waits 1,200 turns between prayers. It also refuses a prayer on an altar of another god, and it refuses again after a rejected prayer until a sacrifice on the wizard's altar. The comment says a prayer that comes too soon costs luck and an experience level.

Seed 4 rises from 0.018 to 0.051. Seed 11 rises from 0.075 to 0.117. Seed 9 falls from 0.255 to 0.018, and from 69,906 turns to 1,403 turns. Seeds 1, 3, 5, 6, and 13 fall from 0.179.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37478334891, wiz-hum-cha-mal, 1 iteration, `--effort high`, corpse walk starts at hungry

[37478334891](https://github.com/OlegPapulov/nethacker/actions/runs/37478334891) finished green. The job ran from 14:21 UTC to 14:53 UTC. The judge scored 0.11444300565928403. The child was not kept. The mean equals the parent. `main` stays on the 0.114 bot.

The operator ran for 1,237 seconds and used 142,799 tokens. The child mean is 36,648 turns. That is the parent turn count. `notes_ignored` is false. `code_unchanged` is false.

The operator changed one existing test. The 20-square corpse walk now starts at `Hunger.HUNGRY`. It used to start at `Hunger.WEAK`. The operator did not add a new action.

All 15 seeds keep the parent progress and the parent turn count. Seed 4 stays at 2,742 turns and 0.018. Seed 9 stays at 69,906 turns and 0.255.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is equal.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37486143597, wiz-hum-cha-mal, 1 iteration, `--effort high`, melee bonus above half hit points

[37486143597](https://github.com/OlegPapulov/nethacker/actions/runs/37486143597) finished green. The job ran from 15:16 UTC to 17:24 UTC. The judge scored 0.10001864934271318. The table printed 0.100. The child was not kept. `main` stays on the 0.114 bot.

The operator ran for 6,927 seconds and used 781,862 tokens. The cold-start mean is 0.114 and 36,648 turns. The child mean is 0.100 and 28,467 turns. `notes_ignored` is false.

The operator changed one line in `melee_monster_priority`. The `+15` melee bonus now requires hit points above `max(8, max_hitpoints // 2)`. It used to require hit points above 8.

Seed 14 rises from 0.075 to 0.255, and from 32,018 turns to 95,414 turns. Seed 0 rises from 0.117 to 0.179. Seed 9 falls from 0.255 to 0.179. Seeds 3 and 5 fall from 0.179 to 0.037 and 0.029. Seed 4 stays at 2,742 turns and 0.018. Seed 8 stays at 9,957 turns and 0.037.

### Why it stopped

A child is kept only when its mean is strictly above the parent. This mean is lower.

### What might solve it

See `experiments.md`. Do not edit `mutator/` until a human approves it.

## Run 37517425932, wiz-hum-cha-mal, 2 iterations, `--effort high`, prayer wait then corpse walk

[37517425932](https://github.com/OlegPapulov/nethacker/actions/runs/37517425932) finished green. The job ran from 19:14 UTC to 20:55 UTC. No child was kept. Each iteration starts from the 0.114 parent.

Iteration 1 scored 0.02384360774531744. The prayer wait goes from 500 turns and from 400 turns to 3,500 turns. Every seed at 0.179 or above falls. Seed 9 falls from 0.255 to 0.018 in 1,403 turns. The operator ran for 2,888 seconds and used 1,001,382 tokens.

Iteration 2 scored 0.10662171848589869. The corpse walk goes from 20 squares to 30. Seed 7 rises from 0.117 to 0.255. Seeds 5 and 6 fall from 0.179 to 0.037. Seed 9 stays at 0.255. The operator ran for 2,539 seconds and used 366,112 tokens.

### Why it stopped

A child is kept only when its mean is strictly above the parent. Each of these means is lower.

## Run 37532568987, wiz-hum-cha-mal, 2 iterations, `--effort high`, corpse cap 25 then melee bonus

[37532568987](https://github.com/OlegPapulov/nethacker/actions/runs/37532568987) finished green. The job ran from 21:15 UTC to 22:39 UTC. No child was kept. Each iteration starts from the 0.114 parent. The assumptions in `GAME_RULES.md` named a prayer wait of 3,500 turns and a corpse walk of 30 squares.

Iteration 1 scored 0.10699510164442977. The weak-hunger corpse walk goes from 20 squares to 25. Seed 0 rises from 0.117 to 0.179. Seed 13 falls from 0.179 to 0.051. Seed 9 stays at 0.255. The operator ran for 2,146 seconds and used 181,479 tokens.

Iteration 2 scored 0.10459918429733958. The +15 melee bonus no longer applies because the monster is faster. It applies only when hit points are above 8 and melee is not fatal. Seed 3 falls from 0.179 to 0.029. Seed 9 stays at 0.255. The operator ran for 1,790 seconds and used 367,142 tokens.

### Why it stopped

A child is kept only when its mean is strictly above the parent. Each of these means is lower.

