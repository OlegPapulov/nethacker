# Next experiment

## Result

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Your task is to raise the score. You use the knowledge in `GAME_RULES.md`. Make one change. That change is one new function, or one rewrite of one function. Do not repeat a listed action. A listed action is a finished measurement. The next change is not a guard for the last death. The next change is one unlisted action that can raise a long game by one experience level. A short game may fall. The mean still has to rise. The one change raises the score. It does not lower the score. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. `experience.md` holds the ends of the played games. Read it and describe why the bot lost. The loss is not the proposal.

**Proposed change (one rewrite):** Increase the corpse-walk distance when hungry (but not weak) from 5 to 10 squares in `agent.eat_corpses_from_ground`.

The hungry state applies while hunger is below weak (Hunger.HUNGRY, i.e. just hungry). Raising this cap allows the wizard to walk farther for food when moderately hungry, reducing starvation on dlvl 1 after local corpses are exhausted. This can help long games survive longer and reach one more experience level without materially changing combat against dangerous monsters. The fainting/weak case remains at 20 squares (unchanged). This change is unlisted (the measured neutral change was only 5→6; 5→10 is different and unmeasured).

- Function rewritten: `Agent.eat_corpses_from_ground` (in `autoascend/agent.py`), specifically the branch `if not only_below_me and self.blstats.hunger_state < Hunger.WEAK:` sets `max_dist = 10` (was 5).
