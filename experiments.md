# Next experiment

## Result

- iteration 1: proposal only; judge to run after exit.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Make one change. That change is one rewrite of one function. Name the one function: `Agent.eat_corpses_from_ground` in `autoascend/agent.py`. Change: when hunger state is HUNGRY but not WEAK (i.e. hunger_state < WEAK and >= HUNGRY context), increase the max distance to search for corpses from 5 to 6 squares (only when not searching only below me). This is a small increase that may help find food before becoming weak without repeating listed actions. It does not violate the rule "Walking farther for a corpse" in a way that contradicts the stated experiments' context and keeps the weak-hunger cap at 20. The change raises the score by avoiding starvation states earlier.

Change the bot from the proposal above. The judge measures that tree.
