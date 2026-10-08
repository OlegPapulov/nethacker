# Playthrough

Identity: `wiz-hum-cha-mal` (Wizard, Human, Chaotic, Male)

The bot follows a strategy built around farming experience on early dungeon levels of Doom (DL1/DL2) until reaching experience level 12 before descending. It relies heavily on eating corpses from the ground for nutrition, as ItemPriority skips picking up corpses and inventory food is limited. The strategy progresses through milestones: farm DL1→find Sokoban→find Mines→etc., with special handling to latch to DL2 when fainting with no edible corpses in reach (within 20 squares).

## Games analyzed (from experiment history)

The judge evaluates 15 seeds. Best recorded mean score was 0.114. Key observations from prior runs:
- Games often stop due to starvation/low HP on DL1 when edible corpses are exhausted (too old/rotten beyond the 50-turn freshness window) and no food remains nearby.
- Progress (milestone reached) is tied to experience level on early floors - waiting until level 12 on DL1 improved mean from ~0.080 to ~0.114.
- Corpses past ~50 turns are inedible/rotten (poison risk); lizard and lichen corpses are exempt from rotting.
- When weak/fainting with no nearby edible corpses (within ~20 squares), latching to DL2 can rescue some runs.

## Why games lost

1. **Hunger/starvation on DL1**: Corpses are the only reliable food source early. Once nearby fresh corpses are consumed and remaining corpses are too far away or too old (>50 turns), the wizard enters WEAK/FAINTING states. With no ranged attack and low HP, this leads to death.
2. **Premature descent**: Descending into Sokoban/mines before banking sufficient XP on Doom floors significantly reduces the final score (progress measured by highest milestone/XP). The bot now waits until level 12, which matches the empirically optimal threshold for these seeds.
3. **Inefficient corpse-seeking**: Going too far to find corpses wastes turns (and risks aging), while not going far enough when weak causes starvation. Prior experiments show capping weak-hunger corpse walks at 20 squares is better than unlimited or much smaller caps.
4. **Energy/casting trade-offs**: Wizard spells cost energy and can misfire; enabling force bolt casts hurt performance (0.0532 vs 0.0694), so the bot avoids casting offensive spells in favor of melee and survival.

## What might solve remaining losses

- Fine-tune corpse search distances and hunger thresholds to balance food acquisition vs turn waste.
- Improve detection of when no edible corpses remain in reach to trigger latching to DL2 earlier or more accurately.
- Avoid behaviors that waste turns exploring unseen tiles before necessary searches (experiment showed this hurt significantly).
- Continue to prioritize banking XP on safe Doom floors until optimal level before descending. 

See `experiments.md` for detailed experimental history and proposed changes.
