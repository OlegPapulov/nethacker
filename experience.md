# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note, so this note states no death for those
games. What follows is the pattern the agent's own replays show; it is not a
death this note records.

The character is a chaotic male human wizard. It has one usable ranged attack
(force bolt) and a weak melee, so the only floor it can level on safely is the
first one. The games end whenever the wizard is taken off that floor. Two ways
that happens are built into the game rules on the first levels: a hole or a
trap door drops it one to three levels down, and a magic trap, a teleportation
trap or a level teleporter moves it away. Below the first levels the monsters
kill it before it can climb back.

## What is the problem

The bot normally refuses to walk onto any known trap. It drops that refusal
inside a short escape window, and at that point it will walk onto the traps
that change floors, which is where the run is lost.

## What might solve it

See `experiments.md`.
