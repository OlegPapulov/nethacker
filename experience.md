# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The 15 played games from the parent evaluation (`parent-eval.json`) all end in death. Most games spend tens of thousands of turns on the farm floor (depth 1) and end right there, mid-fight.

Per-seed ends:

- seed 0: Xp10, depth 4, ~57k turns, killed by a coyote.
- seed 1: Xp11, depth 1, ~67k turns, killed by a dwarf lord.
- seed 2: Xp8, depth 1, ~34k turns, killed by a bolt of fire.
- seed 3: Xp11, depth 1, ~60k turns, killed by a fire ant.
- seed 4: Xp2, depth 2, ~2.7k turns, killed by a goblin.
- seed 5: Xp11, depth 1, ~92k turns, killed by a soldier ant.
- seed 6: Xp10, depth 3, ~69k turns, killed by a hobbit.
- seed 7: Xp10, depth 3, ~60k turns, poisoned by a rotted rothe corpse.
- seed 8: Xp6, depth 1, ~10k turns, killed by a newt.
- seed 9: Xp11, depth 3, ~70k turns, killed by an invisible Mordor orc.
- seed 10: Xp4, depth 2, ~6.3k turns, killed by a kitten.
- seed 11: Xp8, depth 4, ~24k turns, killed by a pony.
- seed 12: Xp5, depth 2, ~5k turns, killed by a kobold lord.
- seed 13: Xp10, depth 5, ~49k turns, killed by a dwarf lord.
- seed 14: Xp8, depth 1, ~32k turns, killed by a bolt of cold.

The ends that matter for the score are the games that already reach the top milestones: seven games reach Xp10-11, and five of them still die in melee (ants, orc, hobbit, dwarf lords) after 50k-92k turns. The wizard's ranged attack (force bolt) is the missing escape: these are the Xp>=10 depth-1 games whose farm streak is a permanently crowded floor, so the quiet moment the strategy waits for never comes and the spell stays dead for the last tens of thousands of turns. Corrupted-corpse, bolt-of-fire/cold, and early-floor deaths follow it.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches. Seven games already sit at Xp10-11; the gap to the next milestone up is large, and the four Xp11 games die at the farm exit instead of completing it. A stable improvement must rescue the crowded-floor melee deaths rather than the already-rare early deaths.

## What might solve it

See `experiments.md`.
