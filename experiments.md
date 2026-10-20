# Next experiment

## Result

- iteration 1: 0.063 not kept (no-cell-improved). Decreases the mean by 0.001 (from 0.064 to 0.063). Moved the weak-hunger eat step to the front of the strategy list.
- iteration 2: 0.060 not kept (no-cell-improved). Decreases the mean by 0.003 (from 0.063 to 0.060). Lowered that threshold from weak to hungry.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). Added a corpse-distance cap that the weak-hunger gate never reaches.
- iteration 2: 0.063 not kept (no-cell-improved). Decreases the mean by 0.002 (from 0.064 to 0.063). Raised several flee and Elbereth thresholds and ate more corpses from the pack.
- iteration 1: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The tree matches the seed.
- iteration 2: 0.064 not kept (no-cell-improved). Does not change the mean (0.064). No code change. The agent wrote a notebook and left the parent in place.
- iteration 1: 0.077 kept (registered). Increases the mean by 0.013 (from 0.064 to 0.077). Capped a weak-hunger corpse walk at 20 squares.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). The judge table matches iteration 1.
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). No code change.
- iteration 2: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Read the spell menu and deleted the cast.
- iteration 1: none not kept (gate:child identical to parent). The tree matched the parent, so the judge did not run.
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Resubmitted the spell-menu tree. The 15 seeds match the parent.
- iteration 1: 0.077 not kept (no-cell-improved). Does not change the mean (0.077). Drew a negative ring for a fast adjacent monster. The 15 seeds match the parent, because melee is still worth 16.
- iteration 1: 0.040 not kept (no-cell-improved). Decreases the mean by 0.037 (from 0.077 to 0.040). Visited unseen tiles before a search. Seeds 10 and 12 rose. Seed 13 fell from 0.179 to 0.024.
- iteration 1: 0.080 kept (registered). Increases the mean by 0.003 (from 0.077 to 0.080). Latched onto dungeon level 2 when fainting and no edible corpse was within 20 squares. The melee function did not change.
- iteration 1: 0.114 kept (registered). Increases the mean by 0.034 (from 0.080 to 0.114). Waited for experience level 12 before it left the first Doom level. Seeds 4, 8, 10, and 12 did not change. Seed 14 fell from 0.117 to 0.075.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Changed the launcher penalty. The 15 seeds match the parent.
- iteration 2: none. The job was cancelled at 360 minutes. No score.
- iteration 1: 0.114 not kept (no-cell-improved). Does not change the mean (0.114). Submitted the launcher edit again. The 15 seeds match the parent.

## Why it stopped

The parent batch is not in this note.

## What is the problem

Mean progress is unknown. The bot is kept only if the next mean is strictly higher on `wiz-hum-cha-mal`.

## What might solve it

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. A child is kept only when that mean is strictly higher. Your task is to raise the score. You use the knowledge in `GAME_RULES.md`. Make one change. That change is one new function, or one rewrite of one function. The change is one small step up the score. Keep the step only when the mean rises. Do not repeat a listed action. A listed action is a finished measurement. A listed action covers the measured situation and a similar situation. A similar situation is the same action. The one change raises the score. It does not lower the score. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. `experience.md` holds the ends of the played games. Read it and describe why the bot lost. Propose one change in this file, in accordance with the game rules. Name the one function you add or the one function you rewrite. Change the bot from that proposal.

### Proposal: give the farm floor's exhausted loop a turn, so the episode never stalls

The farm floor is the whole score. `current_strategy` keeps the wizard on
dungeon level 1 (or the once-latched level 2) until experience level 12. On an
old floor whose map is fully seen and whose search priority has bottomed out,
`open_visit_search` eventually finds no `to_visit` and no `to_search` tile whose
priority clears `search_prio_limit`, so it yields `False`; the surrounding
`repeat()` sees a false condition and returns; `global_strategy` returns; and
`main()` goes back around its loop, presses `ESC` twice, and calls
`global_strategy()` again. `ESC` is not a game turn. So the in-game turn count
stops rising while env steps keep climbing. The arena aborts a seed when the
turn count has not moved for `10_000` env steps, and an aborted seed scores 0.
Every existing preempt on the farm path (`gather_items`, `untrap_traps`,
`search_neighbors_for_traps`, `eat_*`, `cure_disease`) is condition-gated on
something that can be absent (no item, no trap, not hungry, not diseased), so
none of them is guaranteed to take a turn once the floor is exhausted. The bot
can therefore sit in a zero-turn loop and lose the seed outright, or lose the
turns it could have spent pushing the floor's search count forward to reach the
next XP level.

The fix is one new function, `stall_guard(self)`, a strategy that is *always*
entered on the farm floor and always spends one real turn. It reads a
turn-based inactivity counter that `update()` already maintains —
`self.agent._last_turn` is the last turn number and
`self.agent._inactivity_counter` counts consecutive env steps since that turn
last changed — and, once that counter crosses a threshold well below the
arena's `10_000`, it takes a single turn. On dungeon level 1/2 it `search()`es
(the cheapest turn, and one that also nudges the floor's `search_count` toward
the next `to_search` tile); off the farm floors it `move('.')`s to wait a turn
without moving into unknown terrain. This converts an idle stall into continued
play. Because progress is monotone (the scorer keeps the maximum milestone ever
seen), adding a turn to a seed that would otherwise stall weakly cannot lower the
mean — the only tail risk is a bot error or an invalid action, which the low
threshold and the search/wait choice avoid. The function is placed outermost in
`global_strategy`'s preempt chain so it is checked on every loop, and it yields
`True` only once the counter is high, so it is invisible in normal play and
never competes with combat, eating, or exploration.

Self-check against `GAME_RULES.md`: this does not touch the food latch, the
experience gate, the corpse reach, force bolt, the trap window, Elbereth,
skill points, the suit, rings, the melee bonus, the corpse cap, or prayer. It
adds one new function and changes no listed action. It removes a stall, which
is a loss, and can only add turns.

## Proposed code

```python
    @Strategy.wrap
    def stall_guard(self):
        # The farm floor is the whole score, and the farm loop can reach a fixed
        # point: on an exhausted floor open_visit_search yields False, the whole
        # global_strategy returns, and main() re-enters it after two ESC presses.
        # ESC is not a game turn, so the turn count stops rising while env steps
        # keep climbing, and the arena aborts the seed at 10_000 no-progress
        # steps -- a zero. Every other preempt on the farm path is gated on a
        # condition that can be absent. This strategy is always entered and, once
        # update()'s turn-inactivity counter has climbed, spends exactly one real
        # turn (a search on the farm floors, a wait elsewhere). One added turn on
        # a seed that would otherwise stall weakly cannot lower the mean, because
        # progress is monotone; and on a floor that is still explorable it never
        # fires, so it costs nothing.
        if self.agent._inactivity_counter < 150:
            yield False
        yield True

        if self.agent.current_level().dungeon_number in (Level.DUNGEONS_OF_DOOM,):
            self.agent.search()
        else:
            self.agent.move('.')
```

Change the bot from the proposal above. The judge measures that tree.
