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

## Proposal

**Do not refresh the recorded age of a corpse that has already rotted.**

In `Agent.eat_corpses_from_ground` (`autoascend/agent.py`), after the wizard walks to a
corpse it found, the parent overwrites the corpse's recorded age with `self.blstats.time`
whenever the corpse is lying below the wizard and no pet is adjacent. The recorded age is
stamped no earlier than the kill (the kill detector writes `self.blstats.time`, the
"corpse under me" restore at `agent.py:609-618` only ever keeps the *older* value, and the
`defaultdict` default is `-10000`). So the recorded age is always an upper bound on the
true age: if it says "fresh", the corpse is genuinely no older than 50 turns; but the
refresh throws that bound away and relabels a corpse that has already aged past the rot
window as "fresh", which makes the wizard eat a rotted corpse and die of poison. That is
exactly how seeds 6 and 7 end.

Change: only refresh when the recorded age still passes `_is_corpse_editable`, i.e.
`if not self.has_pet and self._is_corpse_editable(monster_id, corpse_age):`. This keeps the
original anti-"walk to the same corpse every turn" behaviour for the case it was written
for (a corpse that is still fresh by its own recorded age stays edible) and otherwise falls
through to the existing "nothing here to eat" branch, which forgets the corpse. Seeds 6 and
7 (Xp:11 and Xp:10, the top of the score table) no longer eat a rotted corpse, so they can
keep farming and descend instead of dying to poison. The change touches only the corpse
freshness judgement; it leaves every listed test (the 3500 prayer wait, the 6->9 hp, the
20-square corpse cap, the 20->10 fainting latch, the melee +15, the level-2 faint latch,
the eat-when-monsters->7-squares gate, the wand path/zap penalty, the doorway/corridor
movement bonus, and the wand-of-striking classification) untouched.

## Last iteration

The previous tree scored 0.133 and was not kept. Do not submit that same diff again.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Leave every listed test as it is, including a nearby number in the same function. Do not change a number in an existing test. Add one behavior the listed tests do not already cover. That behavior raises the experience level a game reaches. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
