# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

The parent batch is not in this note. The judge plays the 15 seeds after you exit.

## What is the problem

The score is the mean of those seeds. Progress is the highest milestone a game reaches.

### The fifteen games

Every one of them has `status "completed"`, `end_status "1"` (death) and `error null`.
No seed stalled, crashed, quit or ascended, so the whole mean is decided by *where each
game stopped*, and progress never goes down again inside a game.

| seed | milestone | progress | turns | max depth | cause of death |
| --- | --- | --- | --- | --- | --- |
| 0 | Xp:9 | 0.11705 | 50145 | 1 | poisoned by an orcish arrow |
| 1 | Xp:10 | 0.17910 | 46006 | 1 | killed by a killer bee |
| 2 | Xp:8 | 0.07454 | 34154 | 1 | killed by a bolt of fire |
| 3 | Xp:10 | 0.17910 | 57042 | 3 | poisoned by an orcish arrow |
| 4 | Xp:2 | 0.01848 | 2742 | 2 | killed by a goblin |
| 5 | Xp:10 | 0.17910 | 55705 | 1 | killed by a giant bat |
| 6 | Xp:10 | 0.17910 | 73840 | 3 | killed by a plains centaur |
| 7 | Xp:9 | 0.11705 | 34611 | 6 | killed by a vampire bat |
| 8 | Xp:6 | 0.03689 | 9957 | 1 | killed by a newt |
| 9 | Xp:11 | 0.25480 | 69906 | 3 | killed by an invisible Mordor orc |
| 10 | Xp:4 | 0.02416 | 6313 | 2 | killed by a kitten |
| 11 | Xp:8 | 0.07454 | 23577 | 4 | killed by a pony |
| 12 | Xp:5 | 0.02911 | 5011 | 2 | killed by a kobold lord |
| 13 | Xp:10 | 0.17910 | 48694 | 5 | killed by a dwarf lord |
| 14 | Xp:8 | 0.07454 | 32018 | 1 | killed by a bolt of cold |

Mean progress 0.11444.

**What the table says.**

- Every death is a combat death. Four are ranged (two orcish arrows, a bolt of fire, a
  bolt of cold) and the rest are monsters that take a turn before the wizard does
  (killer bee, giant bat, vampire bat, plains centaur, Mordor orc) or monsters that
  should never be dangerous at all: a goblin, a kitten, a newt, a pony, a kobold lord.
  A wizard dies to a newt only after something else has already taken his hit points
  and his turns away from him.
- Seeds 4, 8, 10 and 12 are over almost immediately: 2742, 9957, 6313 and 5011 turns
  on depth 1-2, stopping at experience 2, 6, 4 and 5. They contribute 0.018, 0.037,
  0.024 and 0.029 to the mean — together they are worth more than the gap between the
  current score and a fifth of a point. Lifting those four to experience 10 would add
  about 0.040 to the mean on its own.
- Seeds 1, 3, 5, 6 and 13 all stop at experience 10 (0.17910) and seed 9 is the only
  game that ever reached experience 11 (0.25480). No seed reached experience 12
  (0.333) or depth 12 (0.206), so both of the next milestones are still unclaimed.
  Turning the five experience-10 games into experience 11 games is worth about 0.025;
  taking them to experience 12 is worth about 0.051.
- Depths stay between 1 and 6. The bot farms experience on the early floors on
  purpose (waiting for experience 12 before it leaves the first level was the last
  change that raised the score), so XP and survival, not descending, decide the score.

### Why the games end

Local runs of this same bot against a plain NLE environment, on arbitrary seeds that
are *not* the judge's private seeds, all end the same way: the wizard runs out of food,
spends the last thousand turns of the game at hunger FAINTING or STARVING, loses a
turn every time he faints, and is killed by whatever is standing next to him while he
cannot act. Six such runs gave hunger totals like `{'OK': 98977, 'HUNGRY': 8999,
'WEAK': 4180, 'FAINT': 662, 'STARVING': 68}` — the game is fine for ninety thousand
turns and then, in the last fifteen hundred, it is over.

The wizard starts with no food at all, so his emergency food is a prayer: a prayer that
is accepted feeds him. `GAME_RULES.md` warns about this twice — "This wizard is chaotic,
so prayer is less safe than for a neutral wizard" and "A god that rejects the prayer
takes an experience level and hit points" — and that is exactly what happens.

Prayer refusal was seen in three of those six local runs, and in each case it was the
last thing that went wrong before the wizard died:

- one run prayed at turns 72447 (accepted), 72986 (accepted) and 73419 — 433 turns
  after the previous prayer — and got `"Thou must relearn thy lessons!"` → `Goodbye
  level 11`, then starved to death 269 turns later;
- another was refused at turn 27840, lost level 8, and died 132 turns later;
- a third was refused 1184 turns after its last accepted prayer with
  `You feel that Anhur is displeased.`, and died of starvation at turn 4402;
- a fourth run was refused *and* got `You are being punished for your misbehavior!`,
  was chained to a heavy iron ball, and its agent thread then raised an assertion and
  fell back to pressing ESC until the episode was cut short.

NetHack's source explains why a refusal is so expensive. `prayer_done()` in `pray.c`
first asks `can_pray()`, which refuses (`p_type 0`, "too soon") whenever the god's
private counter `ublesscnt` is still above 200. Every accepted prayer sets
`ublesscnt = rnz(350)`, and `rnz()` in `rnd.c` has a very long tail: sampled over
400,000 draws, a 400 turn wait is refused **23%** of the time and a 500 turn wait
**13%** of the time. The bot's two prayer triggers used exactly those two gaps — 400
turns when the wizard is fainting, 500 when he is nearly dead — so in the sustained
starvation that ends these games, a refusal is close to inevitable.

Worse, a refusal from praying too soon does `change_luck(-3)` and `gods_upset()`, which
increments `u.ugangr` *and then immediately rolls `angrygods()`*. With anger 1 the roll
splits about evenly between "displeased" and "Thou must relearn thy lessons!" — an
experience level and the maximum hit points that came with it. And `u.ugangr` never
decays with time: `can_pray()` refuses (`p_type 1`) for as long as it is non-zero, so
from then on every prayer is another one of those rolls, and prayer — the food source —
is gone for the rest of the game unless a sacrifice on the wizard's own altar puts the
anger back to zero.

Two smaller, deterministic ways to be refused come from the same function: praying
while standing on an altar of another god makes `can_pray()` score the request as
`alignment = -record`, which is negative, so it is refused outright; and once a prayer
*has* been refused nothing in the bot stops it from praying again as soon as its
400-turn clock expires, straight into the next `angrygods()` roll.

So the mean is held down by a loop: no food → prayer to eat → refused → an experience
level and permanent anger → no more prayer → starvation → death by whatever is nearby.
That loop is present in the four short games, and it is what stops the five
experience-10 games and the one experience-11 game from going further.

## What might solve it

See `experiments.md`.
