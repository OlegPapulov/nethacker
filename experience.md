# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

This note states no game end, so nothing here invents a death.

The only evidence of how the games end is the measured history in `experiments.md`: the
XP gate at 11, 12 and 14 produces byte-identical runs at 0.114, so no game reaches
experience level 12 while farming the Doom floors. Whatever ends the games ends them
before level 12, one or two experience levels below the 0.255 that level 11 pays and the
0.333 that level 12 pays.

One way a game ends there leaves no trace in any file: an unexpected error inside a
strategy re-raises out of the agent thread, the arena adapter then has nothing left to
hand out but ESC, no further game turn is ever played, and the run is cut off at the
no-progress abort with only what it had already banked. The agent recovers from
`AgentPanic` (ESC twice, `on_panic()`, re-enter the strategy) but not from anything else.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches,
and it never falls, so a game that keeps playing after a recovered error can only hold
or raise its score.

## What might solve it

See `experiments.md`.
