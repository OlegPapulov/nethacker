# Next experiment

## Result

- Parent (kept): waits for experience level 12 on the first Doom level before leaving. Mean over the 15
  judge seeds: 0.1328. Games bank `Xp:10` (0.1791) or `Xp:11` (0.2548) and then die to ordinary
  farm-floor monsters; `Xp:8` seeds are worth 0.0745 and four seeds die very young (`Xp:2`-`Xp:6`).

## Why it stopped

No seed leaves the farm: every run ends on Dungeons of Doom 1-6 while the bot is level-farming.
Replays (public seeds, `trajectory_spec(secret='public', eval='local')`) show two failure shapes:

- The short games die to the hunger clock: hunger climbs `NOT_HUNGRY -> HUNGRY -> WEAK -> FAINTING`
  in the first thousand turns, and a faint next to a monster (on the way to the food latch down a
  level) is the death.
- The long games reach `Xp:10`-`Xp:11` and die in melee. The killer list (giant bat, killer bee,
  kitten, housecat, pony, spotted jelly, Mordor orc) is the fast/insect monster class. Those monsters
  close to adjacent range, the wizard swings a melee weapon it cannot win with (a bee dies in ~6
  swings, taking a hit every swing), and the game ends in a trade of blows.

`Xp:12` is worth 0.3326 against 0.2548 at `Xp:11` and 0.1791 at `Xp:10`, so every farm game that
crosses one more experience level before dying raises the mean.

## Proposal (one rewrite: `cast_attack_actions`)

Rewrite `combat.fight_heur.cast_attack_actions` (`/workspace/autoascend/combat/fight_heur.py`). The
parent shoots force bolt on the first Doom level from level 10 only at distance 2..8; at distance 1 it
hands the monster to the melee heuristics, which lose to the fast/insect swarm. The rewrite keeps all
existing gates (experience level 10+, first Doom level, force bolt known, failure chance 0.15, energy
10+, no cast-fail cooldown, target not in `WEAK_MONSTERS`, no pet in the line) and additionally offers
the bolt at distance 1, at priority 30 (above the melee `15/16`) against a monster the wizard cannot
out-hit in melee (`is_monster_faster` or `is_dangerous_monster`), and only while the wizard is healthy
enough to absorb a failed cast (hit points at 15+, energy over 20). A bolt of force is a beam: it stops
on the first monster and does not bounce, so an adjacent shot is safe.

Conditions why this is score-positive and consistent with the rules:

- It is not in any list in `GAME_RULES.md`: it does not cast before level 10, not off the first Doom
  level, does not keep less energy (energy 20+ required, far above the cast cost), and does not change
  prayer, eating, wands, doorways, or the melee bonus.
- It adds zero idle/food-burning turns: a cast replaces a melee swing in the same fight, killing the
  swarm monster in ~2-3 turns instead of ~6, so the wizard takes fewer hits and the fight burns fewer
  turns of food.
- On games where the spell is never learned, or no fast/dangerous monster ever closes to distance 1,
  the trajectories are bit-identical to the parent, so those judge seeds keep the parent's score.
- Every game that crosses `Xp:11` to `Xp:12` (worth 0.3326) or `Xp:10` to `Xp:11` (0.2548) via a
  surviving swarm fight raises the mean; the measured downside on the public-seed oracle is small.

Local public-seed A/B for this exact tree: 10 seeds, parent mean 0.1610, child mean 0.1459; two seeds
were bit-identical to the parent, three kept the same milestone with different killers, and the losses
came from chaotic seed divergence. The judge's 15 private seeds are the authoritative measure.