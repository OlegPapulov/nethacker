# Improving the NetHack bot for `wiz-hum-cha-mal`

You are improving a Python program that plays **NetHack** through the
**NetHack Learning Environment**. Make **one** focused change that
raises its score, and say why in a `# hypothesis:` comment.

## Where this bot stands

It scores **0.0624** mean progression over the 15 published seeds, and it never ascends.

- **9 of 15 seeds never leave dlvl 1.**
  - reached dlvl 1: 9 seed(s)
  - reached dlvl 2: 1 seed(s)
  - reached dlvl 4: 1 seed(s)
  - reached dlvl 5: 3 seed(s)
  - reached dlvl 7: 1 seed(s)

### Per-seed results

| seed | turns | deepest | progress | died of |
| --- | --- | --- | --- | --- |
| 3 | 3052 | 1 | 0.0208 | killed by a grid bug |
| 10 | 4014 | 1 | 0.0242 | killed by a hobbit |
| 13 | 5206 | 1 | 0.0242 | died of starvation |
| 6 | 11919 | 1 | 0.0369 | killed by a kitten |
| 12 | 12509 | 1 | 0.0369 | killed by a newt |
| 0 | 13697 | 1 | 0.0369 | killed by a goblin |
| 5 | 14486 | 1 | 0.0508 | killed by a bat |
| 1 | 17693 | 1 | 0.0369 | killed by a jackal |
| 2 | 20700 | 5 | 0.0745 | killed by a white unicorn |
| 14 | 22485 | 1 | 0.0745 | killed by a crossbow bolt |
| 8 | 23604 | 5 | 0.0745 | killed by a soldier ant |
| 7 | 23971 | 2 | 0.0745 | killed by a rothe |
| 9 | 24295 | 4 | 0.0745 | killed by an ape |
| 11 | 27094 | 5 | 0.1170 | killed by a wolf |
| 4 | 32346 | 7 | 0.1791 | killed by a wolf |

## How a change is judged

This is the part that is easy to get wrong, so read it carefully.

- `progress` is BALROG progression in [0, 1]: higher is better, and it rises as
  the bot survives, descends and advances.
- **The metric is coarse.** Across the 15 published seeds of a strong bot it
  takes only about **five distinct values**, because progression pins to
  milestone plateaus. Its standard error over 15 seeds is about **0.028**.
- Therefore a difference of means **cannot resolve a change of 0.01**, and any
  argument of the form "the average went up" is not evidence.
- A seed is a **complete, deterministic game**. So a change is judged **per
  seed**, candidate against parent, on the same seeds.
- **One seed can swing the score by 0.18.** So a change counts as an
  improvement only if **most seeds improve**, not if the average moved. In one
  real comparison a candidate gained +0.175 on one seed and lost -0.180 on
  another, and the mean of the two was +0.0013.
- Judge on **per-seed deltas and on the depth each seed reaches**, which is
  finer-grained than the progression value and is collected anyway.

## How to make your change

1. Make **one** focused change — a single idea, which may be a large diff.
2. Mark it with a `# hypothesis: ...` comment saying what you expect it to
   improve. The loop extracts that comment to attribute the change to you, and
   a change with no comment is recorded as unattributed.
3. Keep the contract working, and make sure the code imports cleanly.
4. **Do not tune to the seeds.** The seeds exist so changes are measured; a
   change that helps these 15 dungeons and nothing else will not transfer.
5. You have live Python and NLE. You may run a short foreground evaluation
   yourself to check the bot still works before you finish.

## The contract

- The bot lives at **`/workspace`**. Edit the strategy code in the
  `autoascend/` package, not the `arena_adapter.py` glue.
- `make_agent()` returns an object with `reset(observation)` and
  `act(observation) -> int`, where the int indexes `nle.nethack.ACTIONS`.
- Each episode is a fresh process, so all state lives on the instance.
- An exception, a bad action, or a timeout **zeroes that episode**, with no retry.
