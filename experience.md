# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit. This file does not record a final message for any seed, so no single death is claimed here.

## What is the problem

The games that set the score end on the first dungeon levels, and every one that is not cut short stops making progress at experience level 9. Dungeon level 1 holds only weak monsters -- a lichen, a newt, a grid bug, a jackal, a fox, a goblin, a sewer rat -- and its corpses are the only food. Once the wizard has killed what the first floor holds and eaten the corpses that are still within the 50-turn freshness window, the floor offers no more experience and no more food. The food latch then moves the farm target one level down, but it latches there: `_xp_farm_level` is set to 2 and never changes. A wizard that also out-eats dungeon level 2 starves on it and banks nothing beyond the level it already reached. So the run is bounded by the experience the first Doom floor can give, which is level 9 (0.117); no seed reaches level 10 (0.179) or level 11 (0.255), and the level-12 farming gate is never rewarded.

How the bot loses is therefore the same shape each time: it exhausts the food and the monsters of a farm floor and cannot get more of either, rather than being killed mid-fight at full strength. Because progress is the highest milestone ever reached, the experience banked before that point is what the score keeps.

## What might solve it

See `experiments.md`.
