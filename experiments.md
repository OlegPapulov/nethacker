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

The score is the mean of the 15 judge seeds. The mean falls when a long game loses a milestone, even when a short game lasts longer. Progress is the highest milestone a game reaches. Experience level moves that score. Seed 9 is at Xp:11. Seed 4 dies at 2,742 turns and stops at Xp:2. Seeds 10 and 12 die under 10,000 turns. Leave the weak-hunger corpse walk capped at 20 squares. Leave `_xp_farm_level` as it is. Leave `experience_level >= 12` as it is. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

### Proposal (the one change)

**Never engrave Elbereth.** Make `Agent.can_engrave()` (`autoascend/agent.py`)
return `False`, so `fight_heur.elbereth_action` -- which is the only caller and
which lives in a file this edit may not touch -- never offers the engrave
action, `agent.py:1251-1254` never runs, `engraving_below_me` never becomes
`'elbereth'`, and the wait branch at `agent.py:1255-1259` becomes unreachable.

Why this is the change: the engraving is offered only in the middle of a losing
fight (`hp < 30` with a non-weak monster already adjacent,
`combat/fight_heur.py:201-226`), and once it is underfoot every melee, ranged
and zap loses 100 priority (`fight_heur.py:245-246`, `:257-258`, `:195-196`)
while standing still is worth `30 - 40 * hp/max` (`fight_heur.py:229-234`).
At the hitpoints where the wizard is actually in danger that wait also beats the
retreat rings (never worth more than +10), so the wizard gives up swinging and
gives up running in the same moment -- it can only wait to be killed, and
waiting deals no damage, so the fight cannot end in its favour. Elbereth only
turns away undead, and none of the fifteen killers are undead: a killer bee, a
giant bat, a plains centaur, a kitten, a pony, an invisible Mordor orc. The one
undead death in the parent batch (seed 7, vampire bat) happened with Elbereth
available, so the engraving has no observed payoff and a large observed cost.

Why it cannot cost a milestone the parent banked: the engrave, the `-100`
penalties and the wait only ever fire when `engraving_below_me == 'elbereth'`,
and the engrave is the single write path that sets it. With `can_engrave()`
false the fight is fought with the parent's normal actions instead -- melee at
its usual 16, retreat rings unchanged -- which is what the wizard does in every
fight where it did not engrave, and those fights are where the long games come
from. The change is one gate on one function; it adds no branch on seed, depth,
or turn number, and it leaves the corpse-walk cap, `_xp_farm_level` and the
`experience_level >= 12` gate untouched.

Change the bot from the proposal above. The judge measures that tree.
