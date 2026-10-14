# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

The games I could play myself (arbitrary seeds, run locally through the same
environment, not the judge's seeds) all end on the first dungeon levels, most of
them on dungeon level 1. A game ends when the wizard dies, or when it runs out of
steps. In every case the run stops long before the second staircase down.

The ends I saw, by seed:

- killed by a giant ant (three games), a giant rat, a kobold lord, a werejackal,
  a hill orc, a rothe;
- poisoned by a rotted hill orc corpse;
- killed by a gas spore's explosion (two games);
- one game reached the step limit still alive on dungeon level 1.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game
reaches, so an early death freezes the score at whatever experience level the
wizard had reached.

Two shapes of loss dominate:

1. **Death in melee while starving.** The wizard exhausts the food on the first
   floor and its hunger runs down to WEAK and then FAINTING at full hit points.
   While fainting it is helpless for long stretches, and a monster that walked up
   (a giant ant, a werejackal) finishes it. The food latch rarely fires in time,
   because a corpse usually still looks edible and reachable.

2. **Death to an exploding monster.** A gas spore (and the three spheres) explodes
   on death and blasts every square that touches it. The wizard walks into one and
   either melees it or fires a wand at it from arm's length; the killing blow is
   also a hit on the wizard. In the two games above the wizard was at full health
   and the blast alone killed it, and in one of them two adjacent spores chained.

## What might solve it

See `experiments.md`. The surviving levers must leave the food economy, the weak
melee rule, the corpse freshness rule, and the wand rules as listed in
`GAME_RULES.md`. The exploding-monster leap is not in the list of actions that
lower the score: the rules forbid walking into a fast monster, but they do not
ask the wizard to trade blows with a monster that explodes.
