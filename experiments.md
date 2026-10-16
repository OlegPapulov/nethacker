# Next experiment

## Proposal

Add one function, `keep_healing_spell` (in `autoascend/agent.py`), and register it
once in `autoascend/global_logic.py` just above `keep_attack_spell_memorized`.

The wizard starts with two spellbooks. The first is force bolt, which the parent
already re-learns on the farm (`keep_attack_spell_memorized`). The second is a
healing spell (`extra healing` on some seeds, `healing` on others) and it is dead
weight: like force bolt it lapses about 20,000 turns after it is learned and its
book is dropped early, and nothing in the agent ever reads it again, so the only
healing the wizard has is the emergency potion below one third of maximum hit
points. The new function does for the healing half of the kit what
`keep_attack_spell_memorized` does for the damage half:

- from experience level 10 (the farm) it finds the dropped book on the current
  level, walks to it, takes it to read it, and lets the item priorities drop it
  again, tracking success in the existing `_last_spell_read_turn` /
  `_spell_read_fail_turn` bookkeeping; then
- once the spell is fresh it casts it with `cast(spell, direction=(0, 0))` (both
  healing spells are immediate) whenever the wizard is below 60% of maximum hit
  points and has at least 5 energy.

No new state and no new gates on turned-off floors: it is inert below experience
level 10 so the early games play exactly like the parent, and it only fires for
the seeds whose second book is a healing spell.

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

The 15 judged games all end on the first dungeon levels, and the long ones end in
melee with the wizard taking blows it cannot heal. The wizard's advantage --
spells -- is only half used: the parent re-learns force bolt but never touches the
second (healing) spellbook the identity is given. Keeping that spell memorized
and casting it when hurt is an unlisted action that can let a long game survive to
the next experience level.

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
