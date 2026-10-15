# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The bot dies early on the first dungeon floors. On dlvl 1, food is limited to fresh corpses of weak monsters (lichen, newt, grid bug, jackal, fox, goblin, sewer rat). When those corpses rot past ~50 turns they become inedible/poisonous for most monsters, and lizard/lichen corpses are the only exceptions that remain safe long-term. The wizard farms dlvl 1 (and can latch to dlvl 2 when fainting with no edible corpse in reach) until experience level 12, but starvation still claims many seeds before reaching higher milestones. Additionally, with no strong ranged attack until force bolt is available/castable and with metal armor making spells fail more, the fragile human wizard dies to faster melee threats (e.g. bats, dogs, cats, insects) in open rooms or when forced to fight multiple monsters. Traps on early floors also contribute to deaths.

## What is the problem

The score is the mean of 15 seeds. Progress is the highest milestone a game reaches. The current behavior already implements key raising actions (stay until level 12 on dlvl1, food latch to dlvl2 when fainting with no edible corpse in reach, cap weak-hunger corpse walk at 20, skill points to wielded weapon, force bolt logic, floating-eye zap penalty, trap window blocking). To strictly raise the mean, we need one targeted change that improves survival/food security on the early farm floors without violating any listed lowering action or repeating listed actions.

## What might solve it

See `experiments.md`.
