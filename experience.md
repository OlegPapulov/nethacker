# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## What is the problem

The mean score has plateaued at 0.114. Progress is gated by experience level:
the bot can reach xp9 but cannot consistently reach xp10, xp11, or xp12 on
the first floor farm. Deaths occur on the farm floor where the weak melee is
still the limiting factor (starvation from an exhausted floor is a recurring
pattern in those games).

## What might solve it

The bot picks up every ring and amulet it finds (ItemPriority includes both
classes), but `wear_best_stuff()` only considers the seven armor slots. The
wizard never puts on rings or amulets, so it forgoes easy armor class and
melee bonuses that would help it survive/kill on the first floor farm.
"Armor class still matters" (GAME_RULES.md line 77). Adding a mechanism to
equip rings and safe amulets should let at least a few of the long games reach
one more experience level and raise the mean score.

See `experiments.md`.
