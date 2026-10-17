# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

The note holds no game ends, so it states no death to describe. What the tree itself shows: the wizard starts the game carrying a spellbook of force bolt and never reads it. The spell never enters the known-spell list -- the cast menu is parsed once at init, while it is still empty -- so the farm-floor cast at experience level 10, the re-read after the knowledge lapses, and every other piece of casting code in the agent sit unreachable from the first turn to the last. The games that set this score end on the first dungeon levels, and in every one of them the wizard's spell is never cast once.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.

## What might solve it

See `experiments.md`.
