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

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Describe the games in `experience.md`. Propose one change in this file, in accordance with the game rules. Change the bot from that proposal.

### Proposal: pray only when NetHack will accept it

Every game in `experience.md` ends in combat, and the four shortest ones end after the
wizard has been starving. Prayer is the wizard's emergency food, and the wizard is
chaotic, so `GAME_RULES.md` warns that a refused prayer "takes an experience level and
hit points". Refusal is exactly what the local runs show, and NetHack makes it much
more likely than it looks:

- `can_pray()` in NetHack 3.6's `pray.c` refuses a prayer (`p_type 0`) whenever the
  god's counter `ublesscnt` is still above 200. An accepted prayer sets
  `ublesscnt = rnz(350)`, and `rnz()` in `rnd.c` has a long tail — over 400,000 samples
  a **400 turn** wait is refused 23% of the time and a **500 turn** wait 13% of the time.
  Those were the bot's two prayer gaps: `is_safe_to_pray(400)` when the wizard is
  fainting and `is_safe_to_pray(500)` when he is nearly dead. In the sustained
  starvation that ends these games, a refusal was close to inevitable.
- A `p_type 0` refusal does `change_luck(-3)` and `gods_upset()`, which increments
  `u.ugangr` **and immediately rolls `angrygods()`**: with anger 1 the roll splits about
  50/50 between "is displeased" and "Thou must relearn thy lessons!" — one experience
  level and the hit points that came with it. Observed local runs show both.
- `u.ugangr` never decays with time, and `can_pray()` refuses every prayer while it is
  non-zero. So after one refusal, each later prayer is another ~50/50 roll for an
  experience level, and prayer — the food source — is gone for the rest of the game
  unless a sacrifice on the wizard's own altar puts the anger back to zero.
- Two deterministic refusals come from the same function: praying while standing on an
  altar of another god scores the request as `alignment = -record`, and once a refusal
  has happened nothing in the bot stops it from praying again the moment its 400 turn
  clock expires.

The change is therefore three gates on the existing `Agent.is_safe_to_pray()`, all
taken from NetHack's own rules rather than from any seed:

1. **Wait `PRAYER_MIN_INTERVAL = 1200` turns between prayers** instead of 400/500.
   A 1200 turn wait is refused 2.3% of the time, versus 23% at 400 — a tenfold cut in
   the roll that ends the game, for at most 800 extra turns of waiting.
2. **Do not pray from an altar that is not ours.** `level.altars` already holds the
   real alignment for every altar the bot has looked at; if the standing tile is a known
   different god's altar (or one still marked `UNKNOWN`), do not pray there.
3. **After NetHack refuses a prayer, do not pray again until a sacrifice has appeased
   the god** (and never sooner than 2400 turns). The refusal is detected from the five
   refusal phrases `angrygods()` can print, stored on the agent, and cleared only by a
   prayer that resolves without one.

Nothing about a seed, a monster, a level or a turn number is special-cased; the gates
are the same constants for all 15 seeds.

Change the bot from the proposal above. The judge measures that tree.
