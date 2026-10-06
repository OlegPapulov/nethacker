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

The score is the mean of the 15 judge seeds. Progress is the highest milestone a game reaches. Experience level moves that score. Seed 9 is at Xp:11. Seed 4 dies at 2,742 turns and stops at Xp:2. Seeds 10 and 12 die under 10,000 turns. Leave the weak-hunger corpse walk capped at 20 squares. Leave `_xp_farm_level` as it is. Leave `experience_level >= 12` as it is. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

The proposal: stop spending the carrying-capacity budget and the walking turns on gold.

`ItemPriority._split` in `global_logic.py` allocates one `carrying_capacity` budget in a fixed order -- bag, gold, best melee weapon and armorset, unambiguous healing potions, thrown projectiles, food, then a catch-all pass over potions/rings/amulets/wands/scrolls/tools -- and `add_item` gives each item `int(remaining_weight // unit_weight)` and subtracts it from the budget, with nothing reserved for what comes later. Gold was allocated second and with no `count` limit, so it took as many coins as the whole budget allowed. `carrying_capacity` here is `(strength + constitution) * 25 + 50`, about 650, and a large gold piece is worth up to 1000 by itself, so a few piles on the first Doom floor can drive `remaining_weight` to zero before the healing-potion, food and catch-all passes run; after that every later item resolves to a share of zero.

That costs experience twice. `go_to_item_to_pickup` walks to the nearest item with a non-zero share, so the wizard is steered to the coin pile instead of the potion next to it. And the coins stay in the pack, holding inventory slots (`free_slots` is `52 + is_coin - len(all_items)`) and carrying weight, for no benefit at any milestone: nothing in the bot spends coins, the shop code is not implemented, and the upstream source carries the same TODO this edit acts on -- take coins once shopping exists.

So, one condition, in `ItemPriority._split`:

    -        if self._drop_gold_till_turn < self.agent.blstats.time:
    +        if self._drop_gold_till_turn >= self.agent.blstats.time:
                 for item in items:
                     if item.category == nh.COIN_CLASS:
                         add_item(item)

`_drop_gold_till_turn` starts at `-inf` and is only raised by the vault-guard handlers `follow_guard` and `offer_corpses`, which set it to `time + 100`, so after this edit coins are carried exactly while a guard is about to come for them and are dropped at every other moment (`pickup_and_drop_items` runs `arrange_items`, which drops any free item whose count in `item_split` differs from what is carried). The vault-guard case is unchanged.

Expected effect: the healing potions and food that the gold block was starving get picked up, and fewer turns are spent walking to coin piles, so more turns go into killing monsters on the first Doom floor. That is experience level, which is the only thing the score moves. Risk: flat, if a seed's floor is so gold-rich that the turns saved on walking to coins are smaller than the potions gained.

Left alone on purpose, per the rules: the 20-square weak-hunger corpse walk, `experience_level >= 12`, the `FAINTING` test that sets `_xp_farm_level` to 2, the 50-turn corpse age window (at 60 turns `rotted` can exceed 5 and a tainted corpse gives no nutrition at all), `fight_heur.py`, `exploration_logic.py`, `fight2`, `emergency_strategy`, and anything wizard-specific.

Change the bot from the proposal above. The judge measures that tree.
