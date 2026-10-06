# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note, so the games below are reconstructed from the
judge table kept in `experiments.md` plus the bot's own logging, not from logs of the
parent batch.

The mean is 0.114 against a 15-seed board. The distribution is lopsided and the shape
of it matters more than the mean:

- Most seeds stop in the `Xp:9` band, 0.116987. `newuexp` in `exper.c` is
  `10 * 2**lev` below level 10, so `Xp:9` is 2560 to 5119 experience points and
  `Xp:10` starts at 5120. Seeds sitting just under 5120 are one bad fight from a
  0.117 -> 0.179 jump, and a seed that reaches `Xp:11` is worth 0.254754.
- Seed 9 reaches `Xp:11` and is the best game on the board.
- Seed 13 falls from 0.179 to 0.024 when the bot is made to visit unseen tiles before
  it searches. That single seed, lost to a trap on a floor the bot should never have
  entered, is worth more than the entire mean improvement of the retained gate.
- Seed 14 falls from 0.117 to 0.075 under the level 12 gate, so farming the first Doom
  floor longer is not free on every seed.
- Seed 4 dies at 2742 turns at `Xp:2`, and seeds 10 and 12 die before 10000 turns.
  These three are the early deaths, and they are what holds the mean down: an early
  death at `Xp:2` is roughly a twentieth of a well-farmed run.
- Seeds 4, 8, 10 and 12 are byte-identical across the last two trees, which is the
  signature of a bot that is dying to something that happens early and for the same
  reason every time.

Progress is the highest milestone a game ever reaches, not its state at death, and it
is banked monotonically. So a run can only get worse by dying earlier, and any change
that buys turns of survival on the first Doom floor is worth more than any change that
makes the bot fight better. All three kept changes are of that kind: cap the corpse
walk at 20 squares (+0.013), latch to dungeon level 2 when fainting with no edible
corpse in reach (+0.003), and wait for experience level 12 before leaving the first
Doom floor (+0.034).

## What the games look like

The bot is a chaotic human wizard, so it farms the Dungeons of Doom and never leaves.
`current_strategy` holds `level = (Level.DUNGEONS_OF_DOOM, 1)` for the whole
`BE_ON_FIRST_LEVEL` milestone and exits only when
`blstats.experience_level >= 12`, which no seed has ever reached while farming: seeds
11, 12 and 14 produce identical runs at 0.114. The `_xp_farm_level` latch moves the
target to dungeon level 2, once, when the wizard is actually `FAINTING` and
`has_edible_corpse_in_reach()` is false. `explore_stairs_condition` is
`lambda: False`, so the bot takes no stair it did not already have to take.

A game is therefore a loop of: explore, fight one monster, eat the corpse, repeat, on
one small dungeon floor, until the wizard dies. The fight is `fight2`; the food is
`eat_corpses_from_ground`; everything else is bookkeeping.

Food is the tightest constraint and it is a hard game constraint, not a bot choice.
Corpse rot in `eatcorpse` (`src/eat.c`) is
`rotted = (monstermoves - age) / (10 + rn2(20))`, and `rotted > 5` is tainted: the
corpse is `useupf`'d for no nutrition at all and the wizard is made sick for 10 to 20
turns. At age 50 turns the divisor can be 10, so `rotted` can be exactly 5 and the
window is still clean; at 60 turns it can be 6 and the corpse is worthless. That is why
the parent measured 50 turns at 0.0774, no age check at 0.029 and 500 turns at 0.0496,
and why the window cannot be widened. Lizard and lichen corpses are the exception,
because `nonrotting_corpse` exempts them, and the bot already exempts them.

Hit points are not the constraint the name suggests. `regen_hp` in `allmain.c` heals
the wizard 1 point every 4 turns at experience level 9 and every 3 turns above it, so
between fights it heals on its own and the wizard never needs to rest. What kills it
is a monster that reaches it while it is weak or while it is standing still for the
3 to 9 turns that `eatcorpse` costs, and `emergency_strategy` only quaffs a healing
potion below a third of its hit points and only when no monster is within seven tiles,
because it is preempted below `fight2`.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.

The first Doom floor is a small set of rooms with a few hundred squares, and the bot
spends a large share of its turns there on things that cannot raise its experience
level. The trap search alone is charged per square by `search_neighbors_for_traps`:
`trap_search_offset=1` means one search per unseen plain square and five per unseen
square with an object pile, and the bot gives up on searching only once
`search_diff > 400`, so hundreds of searches go into empty dlvl 1 rooms. Elbereth does
the same thing for free: once engraved, melee, ranged and zap all lose priority and the
wizard waits.

The floor also collects items it cannot use, and one of them is actively taking the
budget away from the things it can.

## What might solve it

`ItemPriority._split` in `global_logic.py` hands out a single carrying-capacity budget
in a fixed order: the bag, then gold, then the best melee weapon and armorset, then
the unambiguous healing potions, then thrown projectiles, then food, then a catch-all
pass over potions, rings, amulets, wands, scrolls and tools. Gold was second.

`add_item` computes `max_to_add = int(remaining_weight // item.unit_weight(...))` and
subtracts what it takes from `remaining_weight`, with no floor and no reservation. The
gold block called `add_item(item)` with no `count`, so it took as many coins as the
whole budget allowed. `carrying_capacity` for this character is
`(strength + constitution) * 25 + 50`, about 650, and a single pile of large gold is
worth up to 1000 in one piece, so a handful of piles on the first Doom floor can drive
`remaining_weight` to zero before the healing potion pass, the food pass and the
catch-all pass ever run. Past that point every later item resolves to
`max_to_add == 0`.

Two costs follow, and neither is experience. `go_to_item_to_pickup` picks the nearest
item with a non-zero share of the split, so the wizard walks to the gold and spends
travel turns on it instead of on a potion. And the coins are carried afterwards: they
occupy inventory slots (`free_slots` is `52 + is_coin - len(all_items)`), they are real
weight, and they are worth nothing to a bot whose score is experience.

Gold is also the one thing in the dungeon the bot has no use for at any milestone.
`emergency_strategy`, the frozen emergency path, will not spend it, the shop code is
not implemented, and the upstream source carries the same TODO this edit finally acts
on: take coins once shopping exists. The one case where carrying coins is right is a
vault guard, and that case is already modelled: `follow_guard` and `offer_corpses` set
`item_priority._drop_gold_till_turn = time + 100` when a guard is visible.

So: invert that one condition, so coins are only carried inside the guard window.

## What I changed

One condition in `ItemPriority._split`, in `global_logic.py`:

    if self._drop_gold_till_turn < self.agent.blstats.time:   # before
    if self._drop_gold_till_turn >= self.agent.blstats.time:  # after

Coins are now taken only while `_drop_gold_till_turn` is still in the future, which is
only after a guard handler has raised it to `time + 100`. Outside that window the gold
block is skipped, `remaining_weight` survives for the healing potions, the food and the
catch-all pass, `go_to_item_to_pickup` stops steering the wizard to coin piles, and
`arrange_items` drops coins already carried, because `pickup_and_drop_items` runs
`arrange_items` on any item under the wizard and any free item whose count in
`item_split[None]` differs from what is carried is dropped.

What I deliberately did not touch: the 20-square weak-hunger corpse walk, the 50-turn
age window, `experience_level >= 12`, and the `FAINTING` test that sets
`_xp_farm_level` to 2. `fight_heur.py`, `exploration_logic.py`, `fight2` and
`emergency_strategy` are untouched, and no spell, reading of the menu, or judgement
about a particular seed is involved, so the same edit applies to every legal
character: no role gains anything from coins and no role loses anything by refusing
them.

What I expect: more healing potions and food on the floor actually get picked up, and
fewer turns are spent walking to gold, which means more turns killing monsters on the
first Doom floor. Both go into experience level, which is what the score is. The risk
is that on a seed whose only floor is a gold-rich one the wizard now walks past coin
piles it would have spent turns on anyway, so the mean could come back flat; if it
does, the next lever on the same budget is to stop the trap search that
`search_neighbors_for_traps` charges per square, not to reopen the gold block.
