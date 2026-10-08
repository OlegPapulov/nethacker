# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not fully in this note; what follows is from games I played (and replayed variants of) on `wiz-hum-cha-mal`.

- Seed 1: 0.179. Banked XP 10 on the Doom floor, then died in melee in a 46k-turn run.
- Seed 9: 0.255. Banked XP 11, the deepest run. It stalls after that.
- Seeds 5 and 6: 0.117. Reached XP 9 and then never banked another level: the farm floor ran dry.
- Seed 14: 0.117. Marginal run; a bad experiment pushed it to 0.075.
- A repeat local seed (12345): XP 7, killed by an invisible hill orc while crossing the floor.

## What is the problem

The wizard is a squishy melee-only fighter on the early floors. Two loss shapes cover almost every seed:

1. Melee deaths on the farm floor. The wizard engages monsters (killer bee, invisible hill orc, gnome zombie, rothe, hobgoblin, giant bat); a faster monster acts before it, and a few hits kill it. When an identified healing potion is in the pack, the parent waits until hit points fall below a third of max (or below 8) to quaff it. By then the fast monster has already taken the first round and the wizard is one exchange from death; the quaff turn is a turn spent not killing.
2. Stalls at XP 9-11. The first two Doom levels hold a finite supply of monsters and corpses. Once the corpses are past the 50-turn freshness window and the last monsters are gone, the wizard can neither eat nor earn XP there, so it stops banking progress.

## What might solve it

Keep the wizard out of the one-to-two-hit kill zone while a healing potion is on hand: quaff an identified healing potion as soon as hit points fall below half of max (instead of below a third). That gives an extra round or two of survivability against the fast monsters that a few hits kills — enough to win the fight or flee and keep farming — without adding any new action or touching the measured prayer, corpse-walk, melee-bonus, farm-latch, or eat-distance tests.

See `experiments.md`.