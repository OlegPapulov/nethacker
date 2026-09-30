# What steering the mutator has taught us

**Human-side log. Not the agent's.** The agent writes `/workspace/experience.md`
inside its own worktree, and that file is the loop's memory — see `AGENTS.md`.
This one is about a different subject: what we have learned by changing the
*brief* and watching what the mutator did. Nothing here reaches the agent, and
nothing here should ever be spliced into a brief.

An entry is worth writing when a run taught us something that would change how
we write the next brief. A finding the agent rediscovered every turn is a
finding about the brief, not about the bot. Cite the run id — the evidence is
committed in `log/<identity>-<runid>.json` and readable with
`python meta/summarize.py <run_id>`.

## The loop

    read this file and meta/experiments.md
      → pick ONE change to loop/brief.py, with a prediction that can fail
      → edit it, copy to the root mirror, dispatch a run
      → settle the prediction from the run's committed numbers
      → record the outcome in experiments.md; promote what generalises to here

A brief change costs ~85 minutes of CI to evaluate, so the loop is manual on
purpose. Automation would generate changes nobody chose to make.

## Findings

### 1. An agent will obey a rule that is stricter than the one scoring it

Run `36637347806`. The mutator made a real change, measured `0.0624 → 0.0671`
(3 seeds up, 2 down, 10 flat), and then **reverted it**, writing "fails the
'most seeds improve' bar, so I reverted it."

The loop's actual rule was the opposite: `mean_gate` keeps anything that
improves the mean, and only a `WIN` demands the per-seed majority. The brief
said something stricter than the harness did, so the agent threw away a genuine
improvement to satisfy a bar nobody was applying.

The generalisable lesson: **a brief that misstates the acceptance criteria
does not merely inform the agent badly, it makes it destroy its own work.** The
brief is not documentation *about* the loop, it *is* the loop as far as the
agent is concerned. When the code changes a threshold, the prose has to change
with it in the same commit, or the agent will be held to the old rule.

### 2. The agent's own factual claims need checking against source

The same run reported "9 of 13 killers have `mmove 12` (max speed)". The
`LVL` macro in `monst.c` is `LVL(lvl, mov, ac, mr, aln)`, so 12 is a *common*
value, not a ceiling — an air elemental is 36. In fact 4 of 12 parsed killers
were at 12, and the faster ones were a bat at 22 and a white unicorn at 24.

The conclusion survived (a monster at 22 cannot be walked away from, so retreat
is capped) but the number it rested on was wrong, and the wrong number had
propagated into our own brief, where we had repeated it as fact.

Two lessons. First, the brief should carry facts we have verified against the
tagged source, and `loop/build_game_rules.py` now derives them and asserts the
alignment constants rather than trusting memory. Second, when the agent asserts
something checkable, check it before repeating it — the agent is a strong
reader of code and an unreliable reporter of the numbers it read off a
struct layout.

### 3. A measured regression should be reverted, and that is not the failure mode

Run `36710578461` also says "Reverted", and this time it was **correct**: the
agent had measured `0.0430` against a `0.0624` parent. It also did something the
previous run did not — it diagnosed before changing. Seed 13 starved at turn
5206 with XP frozen at 89, in FAINTING for ~1150 turns, with 5–10 edible
corpses on the floor and `Inventory.eat` called *zero* times. It named two
concrete defects (`agent.py:1368`, the `del` behind `if not yielded:`;
`global_logic.py:629`, the hunt throttled to `.every(5)`), and then explained
why the fix still lost: the turns spent walking to corpses were the turns the
XP-8 gate needed, and seed 14 collapsed to `0.0000`.

So "reverted" is not a bug signal on its own. The column in `meta/summarize.py`
is a prompt to read the report, not a score. What distinguishes the two runs is
the direction of the measurement, and that is in the report, not the verdict.

### 4. The score is decided by XP, and it is knowable from outside

The mutator read `nethackers/arena/progress.py` and found that on all 15
published seeds the winning term is `Xp`, never `Dlvl`. We had been carrying a
depth ladder as the stated objective since the first commit, on the reasoning
that "progression rises as the bot survives and descends". That reasoning was
half right and led somewhere useless: the family that decides the number is
neither depth nor survival.

This is in the brief now, as the goal, with the evidence. It is the kind of
fact worth re-deriving whenever the identity changes, because "which family
decides" is a property of the seed set, not a law.

### 5. Findings die with the workspace unless something carries them out

`harvest_log` moves a rejected mutant's log to the *next iteration*. Nothing
moved it out of the *run*: run `36710578461`'s 4186 characters — including both
real defects above — were written into a workspace that was deleted when the
job ended. The workflow committed only `log/`, and the artifact path list had
no `experience.md`, so the run's most valuable output was recoverable only by
grepping a 1 MB transcript.

`publish_results` now pushes the surviving parent's log, the history and any
kept tree to `evolve-result/<identity>-<run_id>`. The generalisable point is
narrower than "persist more": **a memory mechanism needs a defined boundary,
and it is easy to cover the inner one and assume the outer one is covered too.**
Iteration-to-iteration and run-to-run are different hops.

### 6. Runs are independent, and that is a choice, not an oversight

Each run seeds fresh from the hub and re-derives what it needs. Iteration 1 of
every run starts with `experience log: 0 chars`. It is tempting to read the
results branch as memory the next run should consume, and it must not be: a
run that inherits another run's conclusions stops testing them and starts
assuming them. Keeping the record durable but not load-bearing is what lets us
check a prediction against what the agent actually concluded, rather than
against what we already thought.

## Open

- The 5-iteration run `36728246238` is the first real test of whether the
  experience log composes: five turns reading and extending one log, rather
  than five independent guesses. Its result is the first thing to write in
  `meta/experiments.md`.
- The mutator has now twice proposed a change the harness scored as a
  regression, having measured it privately first. That is good behaviour, and
  it suggests the private-measurement habit is already established. Whether it
  ever measures a *win* and correctly leaves it in place is untested — both
  observed reverts were of losses.
- `GAME_RULES.md` is scoped to one identity's measured deaths. When the
  identity changes, it has to be regenerated or it will confidently describe
  monsters the bot no longer meets.
