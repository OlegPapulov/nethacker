# Playthrough

Identity: `wiz-hum-cha-mal`

## What the judge actually measures

`nethackers/arena/progress.py` scores an episode as the **highest milestone ever
seen**, not the state at death: `NetHackProgress.update` calls `_record` for
`Dlvl:<blstats[12]>` and `Xp:<blstats[18]>` on every step and keeps the running
maximum (`if value is not None and value > self.progression`). So the score is
`max(all Dlvl values, all Xp values)`.

Two consequences drive everything below.

1. **Experience level dominates depth for this character.** `Xp:11` is worth
   0.2548 while `Dlvl:21` -- the deepest Doom floor -- is worth 0.3789 and
   `Dlvl:12` is 0.2061. A wizard that never leaves Dungeons of Doom level 1 and
   banks experience levels is already scoring more than a level-14 swordsman
   wandering to `Dlvl:20`. On the other hand `Xp:14` is 0.4940 and `Xp:20` is
   0.7174, so on this table the only large moves are **up the XP ladder**.
2. **Nothing can lower a run's score.** Levelling longer is free. That is why the
   `Milestone.BE_ON_FIRST_LEVEL` gate is an XP gate and not a depth gate: the
   measured history in `experiments.md` is 0.080 at `Xp >= 8`, 0.109 at
   `Xp >= 10`, 0.114 at `Xp >= 11`, 0.114 at `Xp >= 12` and `Xp >= 14`.

The score is also zeroed on any bot-attributable failure
(`invalid_action` / `bot_timeout` / `bot_error`, see `arena/trajectory.py::_result`),
so a crashed or wedged thread costs the whole episode.

## The fifteen games

The parent batch is not in this note, so this is what the recorded history in
`experiments.md` establishes about it, seed by seed.

* **Parent mean: 0.114** (sum 1.712 over 15 seeds), reached by the iteration that
  "waited for experience level 12 before it left the first Doom level" (0.080 ->
  0.114). Everything before that change sat between 0.053 and 0.080.
* **Every seed's score is an exact XP value from the table.** Cross-referencing
  the recorded numbers: 0.117 = `Xp:9`, 0.179 = `Xp:10`, 0.075 = `Xp:8`,
  0.024 = `Xp:4`. No seed in the recorded runs is scored by depth, by a Quest
  `Home`, or by the Astral Plane. The Dlvl ladder never once won.
* **Seed 9 ends at `Xp:11`** (0.2548) -- the only seed recorded above `Xp:10`, and
  the one that makes the gate fire. It is why `Xp >= 11` and `Xp >= 12` produce
  byte-identical runs: the seed that reaches 11 leaves for Sokoban, and every
  other seed dies before the gate.
* **Seed 4 dies at 2,742 turns on `Xp:2`** (0.0185). Nearly three thousand turns
  of turns produced under 20 experience points, i.e. a handful of kills, and then
  death.
* **Seeds 10 and 12 die under 10,000 turns.** Under 10,000 turns a level-1
  wizard is still on the first Doom floor; both are early deaths.
* **Seeds 4, 8, 10 and 12 were bit-for-bit unchanged** by moving the gate from
  11 to 12 -- confirming they die before `Xp:11` and are insensitive to anything
  about the later game.
* **Seed 14 fell 0.117 -> 0.075** (`Xp:9` -> `Xp:8`) under the same change, and
  **seed 13 swung 0.179 -> 0.024** (`Xp:10` -> `Xp:4`) when the exploration order
  was touched. Those two swings are the whole spread of the batch: same code
  family, same seeds, ±6 experience levels depending on which fight happens to go
  wrong.

So the shape of the batch is: **a handful of seeds (seed 9, and the `Xp:10`/`Xp:9`
seeds) farm their way to `Xp:9-11`, and the majority die on the first Doom floor
somewhere between `Xp:2` and `Xp:8`.** No seed has ever reached `Xp:12` on the
farm level, which is why the current gate value is inert.

## Why the bot lost

The batch dies early, and the early deaths are not the ones the previous edits
were aimed at. The recorded experiments already close off the food axis: moving
the weak-hunger eat step to the front of the list (0.063 vs 0.064), lowering that
threshold from weak to hungry (0.060), raising flee/Elbereth thresholds, widening
the corpse walk, and widening the corpse freshness window to 500 turns (0.0496 vs
0.0774 at 50) all lose. The corpse walk cap of 20 squares is load-bearing and
`_xp_farm_level`'s fainting test is load-bearing.

What is left is a **combat** failure, and the code contains one that is
unconditional and self-inflicted.

`combat/fight_heur.py` writes Elbereth (`elbereth_action`) and then obeys it
(`wait_action`, plus the `-100` subtracted from `melee`, `ranged` and `zap` in
`get_available_actions` / `get_potential_wand_usages`):

* `elbereth_action` only offers the engraving when a monster is **already
  adjacent** and `hitpoints < 30`. A wizard's `max_hitpoints` is below 30 for
  most of the game and at full health `adj_monsters_count` is multiplied by
  `1 - sqrt(1) == 0`, so the priority is `-15` and never fires. **The engraving is
  therefore only ever written while damaged, with something next to us.**
* Once written, `wait_action` returns `30 - 40 * hitpoints / max_hitpoints`.
  The strongest competing action while the words are underfoot is a `move` worth
  at most 3 from the heatmap (`go_to` is 1, `melee` -84, `ranged` -89, `zap`
  -100). So **below two thirds of our hitpoints, waiting is the highest-priority
  action in the fight**: the wizard cannot strike, cannot shoot, cannot zap, and
  cannot walk away.
* `fight2` only leaves its loop when nothing is within seven squares, and
  `fight2` is preempted *above* `emergency_strategy`, so nothing downstream can
  break the loop. Every monster that reaches us then hits for free, turn after
  turn, until the wizard is dead.

Solving the priority arithmetic for a wizard with `max_hitpoints` 20 and two
dangerous monsters adjacent:

| hitpoints | Elbereth offered? | `wait` priority | frozen? |
|---|---|---|---|
| 19/20 | no | -8.0 | no |
| 15/20 | no | 0.0 | no |
| 13/20 | **yes** | 4.0 | yes |
| 12/20 | **yes** | 6.0 | yes |
| 10/20 | **yes** | 10.0 | yes |
| 8/20  | **yes** | 14.0 | yes |
| 6/20  | **yes** | 18.0 | yes |
| 4/20  | **yes** | 22.0 | yes |

A dangerous+plain pair needs 11/20; two plain monsters need 4/20. A wizard is at
half its hitpoints after one bad exchange, so the engraving is offered in the
middle of an ordinary fight on the first Doom floor.

The result is that a run which reaches a fight it is losing stops playing
NetHack. It stands on the spot where it wrote the words, banks no further
experience, and dies with whatever level it had. That is exactly the recorded
signature: long games that stop early (`Xp:2` at 2,742 turns), and an XP ceiling
of 9-11 that no amount of extra farming ever breaks through.

The bot can only write the words when it holds a marker or a pointed tool, so the
batch is split -- some seeds never pick one up and are untouched by this, which is
also why the damage is spread across seeds rather than uniform.

## What might solve it

See `experiments.md`.
