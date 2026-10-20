# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. No game end, death cause, or turn count is
recorded here, so no specific death can be claimed for the played games. What
the parent batch is known to be is a wizard that farms the first dungeon floor
for experience and scores the mean 0.114 over the 15 seeds. The mechanism that
ends these seeds is not a single recorded death in this file; it is the farm
loop reaching a fixed point. On a fully seen floor whose search priority has
bottomed out, `open_visit_search` yields `False`, `global_strategy` returns, and
`main()` re-enters it after two `ESC` presses — which are not turns. The in-game
turn count stops rising while env steps climb, the arena aborts the seed at
10_000 no-progress steps, and an aborted seed scores 0. That is a loss the note
can describe without inventing a death.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game
reaches. The bot is kept only when the next mean is strictly higher. Any seed
that stalls before it banks a milestone drags the mean down to 0 for that seed.

## What might solve it

See `experiments.md`.
