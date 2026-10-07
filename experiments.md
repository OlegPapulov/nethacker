# Next experiment

## Proposal

The game rules say the word helps after it is on the floor. Across the fifteen games the wizard writes Elbereth seven hundred and six times and the message that a monster has turned to flee instead of striking appears three hundred and eleven times — a repelled monster standing next to the wizard, unwilling to touch it. `get_available_actions` subtracts one hundred from the melee priority of any monster whenever the tile under the wizard reads Elbereth, so on exactly those three hundred and eleven occasions the wizard declines the swing and walks off the engraving instead. The wizard gives away the thing the engraving was written for.

The change is to delete that existing test — the two lines that drop melee by one hundred while standing on Elbereth. A repelled monster is a monster that cannot hit back, so a swing taken there is free damage and, often, a free kill, and a monster that is not repelled is a monster the wizard would be trading blows with off the engraving anyway, where it already prefers to fight rather than run. Nothing else moves: the ranged and wand penalties on the same tile stay where they are, the priority of writing the word itself stays where it is, and the wait action that lets the wizard sit on the engraving while hurt is untouched. No action or strategy is added.

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
- iteration 1: 0.099 not kept (no-cell-improved). Decreases the mean by 0.015 (from 0.114 to 0.099). Deepened the negative ring around a monster in lethal melee range from -5/-10 to -25/-5 so that one step of flight scores above the melee action's 16. Seed 3 fell from 0.179 to 0.029. Seed 0 fell from 0.117 to 0.075. Seed 7 fell from 0.117 to 0.075. Seed 4 rose from 0.018 to 0.021. The other eleven seeds did not change.
- iteration 1: 0.052 not kept (no-cell-improved). Decreases the mean by 0.062 (from 0.114 to 0.052). Gave corridor and doorway tiles one point in the fight2 movement heatmap whenever a real monster was visible. Seed 9 fell from 0.255 to 0.037. Seeds 1, 5, 6, and 13 fell from 0.179 to 0.037, 0.037, 0.021, and 0.037. Seed 3 fell from 0.179 to 0.029. Seed 12 rose from 0.029 to 0.117.
- iteration 1: 0.104 not kept (no-cell-improved). Decreases the mean by 0.010 (from 0.114 to 0.104). Did not subtract 100 from melee while standing on Elbereth, so the wizard swings at monsters the engraving has repelled. Seed 6 rose from 0.179 to 0.255. Seed 12 rose from 0.029 to 0.117. Seed 3 fell from 0.179 to 0.075. Seed 7 fell from 0.117 to 0.051. Seed 13 fell from 0.179 to 0.037. Several others lost small amounts. Gains were offset by losses.

## Last iteration

The previous tree scored 0.104 and was not kept. Do not submit that same diff again.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Change one test that already exists. Do not add a new action. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

Change the bot from the proposal above. The judge measures that tree.
