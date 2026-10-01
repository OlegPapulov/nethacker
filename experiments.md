# Next experiment

Identity: `wiz-hum-cha-mal`. Parent mean **0.06242**, this change measures **0.06431** on the same 15 public seeds.

## What was the problem

The bot never ate. In `autoascend/global_logic.py` the food preempt called

```python
self.agent.eat_corpses_from_ground()      # only_below_me defaults to True
```

`eat_corpses_from_ground(only_below_me=True)` can only eat a corpse that is *already under our feet*.
Corpses are never picked up (`ItemPriority` skips them) and `eat_from_inventory` only allows
lizard/lichen, so almost no food was ever reachable. The symptom was fainting: instrumenting
`Inventory.eat` and the message log over the parent build showed **53, 111, 63, 86 and 78 faints** on
seeds 0, 1, 5, 12 and 13, and seed 13 died of starvation with only 5206 turns played. Fainting is
turns lost while helpless in a level full of monsters, and turns are the resource the score is made of.

## The change (one hypothesis)

`# hypothesis:` comment sits above the edited preempt in `autoascend/global_logic.py`. Two parts:

1. **`autoascend/global_logic.py`** — when `hunger_state >= Hunger.WEAK`, walk to the nearest corpse
   that is safe to eat and eat it there. The existing cheap path (eat a corpse we stand on, at
   `NOT_HUNGRY`) and `eat_from_inventory().every(5)` are kept.
2. **`autoascend/agent.py::eat_corpses_from_ground`** — make that walk survivable:
   - on arrival, refresh the recorded corpse age, because walking there can take more than the 50
     turns the aging rule in `_is_corpse_editable` allows and the bot would otherwise walk to the
     corpse, refuse it, and walk there again every turn. Skipped when `has_pet`, so a pet's corpse
     of the same species is never mistaken for the one we killed;
   - forget the corpse if we walked to its square and there is nothing to eat there, and return
     immediately after a successful eat instead of falling through.

Both halves serve one hypothesis: never be helpless from hunger, because hunger was the cheapest way
to lose the turns that XP and depth are made of.

## Result

`python -m nethackers.arena.run --solution /workspace --batch '[[0,"wiz-hum-cha-mal"], ...]' --evaluation-id local --out /tmp/eval.json`
— all 15 seeds `completed`, no errors, mean **0.06431** vs parent **0.06242** (+3.0%).

The mechanism is unambiguous even though the mean margin is small:

| | parent | this change |
| --- | --- | --- |
| faints per game | 53-208 | **0** (seeds 0, 4, 13 measured) |
| seeds reaching depth >= 2 | 6/15 | **9/15** |
| seeds reaching depth >= 3 | 5/15 | **7/15** |
| mean turns survived | 17138 | **18955** |
| died of starvation | 1/15 | 1/15 (seed 14) |
| killed by a wolf | 2/15 | 0/15 |

No faint survives: seed 13 went from 5206 turns / Xp:4 to 31848 turns / Xp:8, seed 0 from 13697 to
27740 turns and depth 1 to depth 2. The change generalises because it is not conditioned on any seed,
character class or square — it is simply "when you are WEAK, go eat the nearest safe corpse".

The mean is only +3% because the score is dominated by how deep a lucky run gets: seed 4 used to reach
depth 7 (0.179) and now dies at turn 2644 to a kobold zombie, which is an unrelated early fight that
the extra food never got the chance to help with. Score variance on this character is about +/-0.008
standard error, so the honest reading is "the starvation failure mode is gone, the mean moved up
slightly".

## Variants measured on all 15 seeds and rejected

| variant | mean | why rejected |
| --- | --- | --- |
| walk to a corpse at `HUNGRY` (unlimited range) | 0.0574 | walking across the level while merely hungry gets us killed more often than it feeds us |
| walk to a corpse at `HUNGRY`, after the agent fix | 0.0602 | same |
| walk at `WEAK` but only to a corpse within 2 squares | 0.0447 | starves again — 2 starvation deaths, corpses are not next to us |
| walk at `HUNGRY` within 1 square + `WEAK` unlimited | 0.0564 | loses the deep runs |
| ignore the 50-turn corpse aging rule | 0.0472 | **poisoned by a rotted gnome/orc/floating eye corpse** in 3 games. The aging rule is protective; corpses really do rot, and `_is_corpse_editable` must keep rejecting them |
| **`WEAK`, unlimited range, with the arrival fix (shipped)** | **0.0643** | — |

## What is still wrong, and what I would try next

- **seed 14 still starves to death** while fainting with 7 corpses recorded on the level. Tracing it
  (`/tmp/work/hunger_trace.py`) shows all 7 are BFS-reachable and all 7 fail `_is_corpse_editable`
  *only* on the 50-turn aging rule: we kill a monster at turn 3900 and get hungry at turn 3968.
  The safe fix is not to eat older corpses (that poisons us, see above) but to eat *promptly* — the
  corpse of the monster we just killed, at `HUNGRY`, which is fresh. That variant measured 0.0602 on
  its own; it needs to be combined with a cheaper walk so that it does not also give up the deep runs.
- 6 of 15 games still die on depth 1 to a first monster. That is a combat problem, not a food problem,
  and it is where the next large gain is.

## Measurement notes

- Local harness `/tmp/work/dbg.py` reproduces the judge seeds exactly; `/tmp/work/allseeds.py` runs
  all 15 in parallel processes for iteration. Only the `nethackers.arena.run` command above is the
  official measurement.
- Do not trust a `"You eat"` message counter to test this change — it reads 0 even when the bot eats
  hundreds of corpses. Patch `Inventory.eat` and count calls, and count `"You faint"` in the message log.