# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.

## The 15 judge games

The wizard farms experience on Doom dlvl 1 until `experience_level >= 12`, and then
walks back up for the mines. Those are the only scores that matter, because
progress is monotone: the scorer keeps the highest milestone ever seen, so a run
can never lose banked score, and levelling longer can never lower a mean.

Where the 15 seeds actually land under the 0.114 parent:

- Nine seeds sit between `Xp:9` (`0.1170`) and `Xp:11` (`0.2548`). Seed 9 is the
  best of them at `Xp:11`.
- No seed ever reaches `Xp:12` (`0.3326`). The XP-12 gate is measured to be
  unreachable on the Doom floors: seeds 11, 12 and 14 produce byte-identical runs.
- The next milestone the score cares about after `Xp:11` is `Home 1` (`0.3661`),
  so a wizard that reaches `Xp:12` and turns around has already doubled the run.

Three seeds never get a farm going at all:

- Seed 4 dies at 2,742 turns while still on `Xp:2` (`0.0239`). It starves or is
  killed on the first floor before the farm can pay off.
- Seeds 10 and 12 die under 10,000 turns, in the same early stretch.

The mean is therefore `0.114`, and it is dragged down by three dead seeds and by
nine plateaued ones.

## What the plateau is

Eleven of the fifteen seeds stop on one exact experience level, which is not what
death looks like. Death spreads scores; a repeated number means the run ended for
a reason that banks whatever the wizard had at that moment.

That reason is a stall. A stall is a loss in this game (`GAME_RULES.md` line 15),
and it has a precise shape: NLE ends an episode after 10,000 steps during which
the in-game turn counter has not moved (`DEFAULT_NO_PROGRESS_TIMEOUT`). A wizard
with nothing to do takes steps and no turns.

The XP farm makes exactly that state likely. `current_strategy` asks to be on Doom
dlvl 1, and a wizard with the whole first floor dug out and nothing new to find
has nowhere left to go on that floor. `current_strategy` is a generator, so when
every strategy below it yields false it spins in place: no turn, no step budget
left, no way out. The wizard banks the level it happened to have, which is why
so many seeds land on the same number.

Two things make the plateau visible before it happens, and neither needs a turn to
have been missed:

- Doom dlvl 1 does have a down stair. Only the up stair is withheld from it
  (`mklev.c` makes down stairs on every non-bot level). The stairs strategy is
  already in the chain, so a floor below is always walkable once the stair is known.
- `explore1` already knows when a floor is used up. It asks the same question
  twice -- is there a reachable tile left to walk to (`to_visit_func`), and is
  there a reachable tile left worth searching (`to_search_func`) -- and it has a
  ready-made yardstick for "dug out", `search_diff > 400`, the same threshold it
  uses to let the wizard walk over traps without searching them.

So the stall can be prevented rather than diagnosed: when the floor under the
wizard has nothing left on it, move the farm one floor deeper and keep going.

## What might solve it

See `experiments.md`.
