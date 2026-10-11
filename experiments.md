# Next experiment

## Result

- iteration 1: 0.114 kept (registered). Waited for experience level 12 before it left the first Doom level.
- iteration 1: 0.114 not kept (no-cell-improved). Changed the launcher penalty.
- iteration 2: none. The job was cancelled at 360 minutes. No score.
- iteration 1: 0.114 not kept (no-cell-improved). Submitted the launcher edit again. The 15 seeds match the parent.

## Last iteration

The previous tree scored 0.122 and was not kept. Do not submit that same diff again.

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches, and the experience level is the milestone that moves this score. The parent already farms the first Doom level (latching one level down when it is fainting and no edible corpse is within reach) until experience level 12, but no seed ever reaches level 12: every run ends on the farm floor somewhere between level 8 and level 11, so the mean stabilises at 0.114. The gate itself is no longer the limiter -- the bottleneck is that a run banks its highest level before the floor can feed it more kills.

## What might solve it

Make one change. That change is one rewrite of one function: `fight2` in `autoascend/agent.py`.

`fight2` currently ignores every visible monster that is more than 7 BFS squares away (`all(dis > 7 ...)`), even while the wizard is waiting on the farm floor. Those far monsters are pure wasted XP and wasted fresh corpses: they either walk to the wizard at their leisure or the wizard wanders off and they are never fought at all. The wizard is low-level for a long time, and every extra kill on the farm floor is both experience toward the next level (the milestone) and a fresh corpse that keeps the 50-turn food window alive, so the run survives one step longer and banks a higher level.

The rewrite keeps the tuned fight logic untouched. It only replaces the constant engagement distance with one that is wider, but strictly on the floors the parent farms (Dungeons of Doom, depth 1-2) and only while the wizard is healthy enough to walk to a monster (at least half hit points). Everywhere else, and while hurt, the gate stays exactly 7, so the games that end in Sokoban, the mines, or in a weak/fainting state keep the parent's exact behaviour.

## Proposal

Rewrite `fight2` so that, while the wizard is on the first two Dungeons of Doom levels with at least half its hit points, it engages the nearest visible monsters out to a BFS distance of 12 instead of 7. When the wizard is hurt, off the farm floors, or on any branch, the original 7-square gate is preserved unchanged.

Change the bot from the proposal above. The judge measures that tree.