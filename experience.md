# Playthrough

Identity: `wiz-hum-cha-mal`

## Recent games (from experiments)

- Seeds pattern (from last kept iteration): iteration 1 giving 0.114 (kept). Seeds 4, 8, 10, 12 unchanged relative to 0.080 baseline; Seed 14 fell from 0.117 to 0.075. Mean rose +0.034 from 0.080 to 0.114.
- The bot farms XP on first Doom level (dlvl 1) and can latch to dlvl 2 when fainting with no edible corpses in reach within 20 squares (via `has_edible_corpse_in_reach`).
- It waits for experience level >= 12 before leaving the first Doom level (BE_ON_FIRST_LEVEL milestone gate). This is the key change that produced the jump to 0.114.

## Why it stopped / what’s the problem

- Current best registered mean is 0.114 for wiz-hum-cha-mal over 15 seeds. Progress is the highest milestone reached; score is the mean of 15 seeds. The bot is only kept if next mean is strictly higher.
- Farming to level 12 on Doom floors gives strong scores on many seeds (level 10–11 already big jumps), but seed 14 dropped when moving to the level-12 gate. Overall +0.034. The gate is already at 12 (which behaves like the measured best). Further gains likely require a different trade-off, not just raising this gate.
- Food management matters early: bot looks for edible corpses within reach (20 squares when weak/hungry in the corpse-walk logic). Starvation on dlvl1 leads to latching down to dlvl2. Corpse aging/rot constraints (50 turn freshness window, exceptions for lizard/lichen) limit safe eating.
- Wizard is fragile (low HP, metal armor blocks spells, casts cost hunger). Casting was disabled/trimmed; spell list reading added. Melee-focused survival with careful positioning.

## Analysis

The bottleneck is balancing XP farming time vs survival/resources. Going to level 12 on Doom improved mean, but hurt seed 14. The next improvement needs to be subtle: change one existing condition (a test/threshold) rather than adding actions. Possible targets: the corpse-walk distance when weak (currently 20 squares in `eat_corpses_from_ground` for WEAK state; also `has_edible_corpse_in_reach` uses max_dist 20). Or the freshness window (50 turns) is load-bearing. Or the latch threshold/behavior when fainting. Or the XP gate (already at 12). Or the distance caps in non-weak hunger states. All are existing parameters/tests.

The instruction says “change one test that already exists”. Given experiments show small threshold tweaks (distances, hunger thresholds), a good candidate is to tweak an existing distance/cap or an existing conditional threshold by a small amount consistent with game rules.
