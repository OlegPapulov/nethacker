# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The bot dies while farming dungeon level 1, with the longest runs reaching only Xp:10 or Xp:11 and ending to fast dangerous monsters (fire ant, soldier ant, dwarf lord, invisible orc, rothe) or to ranged/thrown hazards (bolt of fire/cold, shattered potion). A few short games fall through to depth 2-5 and die to goblin, kitten, kobold lord, or poison. The mean progress is 0.14829 (based on `refs/parent-eval.json`); to raise it the bot must survive longer or kill more to gain another experience level on some of those long games without lowering others.

## What is the problem

The bot treats already-dangerous monsters (insects/pets) as "imminent death" only when HP <= 16. That threshold is too low for the pace of melee on dlvl 1 while casting force bolt from range is gated by energy, spell fail, and distance. Raising the threshold gives the movement/casting strategy more leeway to disengage and fire from range, reducing early deaths against fast dangerous monsters.

## What might solve it

See `experiments.md`.
