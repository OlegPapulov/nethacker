# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The 15 public seeds are the games. The parent mean is 0.13786. The bot dies on
almost every seed; the deeper games reach Xp:10-11 and the weakest reach Xp:2-6.
After the change below the mean is 0.14320: seed 8 goes from Xp:6 to Xp:9 and
every other seed is unchanged.

## What is the problem

Progress is the highest milestone (experience level) a game reaches, and the
score is the mean over the 15 seeds. Most games end in death within the first
few hundred turns for reasons the parent does not handle: a bolt of fire or
cold, a starving faint at full HP that gets the character punished, a lone weak
monster (goblin, kitten, kobold lord, pony).

The clearest avoidable loss was seed 8. The wizard is on dungeon level 1 with a
wand of magic missile in the pack. When its exploration task stalls the strategy
forces an attack for a few turns so the bot does not loop in place. With no
better option the bot shoots the wand at a nearby floating eye. The eye is
worth almost nothing to kill, but it gazes back the instant it is hit:

    You hit the floating eye!  You are frozen by the floating eye's gaze!
    The newt bites!  ...

The wizard is paralysed and cannot act while an adjacent newt bites it to death.
The game ends at Xp:6 (0.0369) instead of continuing past Xp:8. The eye is not
the threat; the paralysis is, because any monster standing next to the wizard
gets free hits while it is frozen.

## What might solve it

See `experiments.md`.
