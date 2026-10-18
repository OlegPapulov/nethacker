# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## Why the bot lost

The recorded ends are in `/refs/parent-eval.json`. Eleven of the fifteen games end in melee on the early dungeon levels: a rothe at experience level 10, a dwarf lord at 10 and at 11, two soldier ants at 11, a fire ant at 11, an invisible Mordor orc at 11, a goblin at 2, a kitten at 4, a kobold lord at 5, and a pony at 8. Two games end under a bolt of fire and a bolt of cold at experience level 8, one under a poisoned rotted rothe corpse at 10, and one under a shattered potion at 9.

The wizard reaches experience level 8 through 11 hurt and keeps trading blows anyway. The parent engraves Elbereth only below 30 hit points, and its engrave priority loses to the melee value of 16 in nearly every fight, so the fights that end at experience level 10 and 11 never give the wizard a turn to recover: it drops from full health to the killing blow inside one engagement with a rothe, a dwarf lord, or an ant.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.

## What might solve it

See `experiments.md`.
