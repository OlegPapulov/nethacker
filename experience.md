# Playthrough

Identity: `wiz-hum-cha-mal`

## Why it stopped

From the parent evaluation (`/refs/parent-eval.json`), games end on the first few dungeon levels (max depth 1-5). Many deaths occur at low XP: there is a large cluster dying around Xp10–Xp11 (e.g., 0,3,5,6,7,9,13 at Xp10–Xp11) with cause ranging from melee encounters (rothe, dwarf lord, fire ant, soldier ant, Mordor orc, poisoned by rotten corpse) and some early deaths at much lower XP (goblin at dlvl2 Xp2, kitten at dlvl2 Xp4, kobold lord at dlvl2 Xp5, pony at dlvl4 Xp8). A few are killed by bolts/traps (fire/cold/shattered potion).

The parent tries to farm on dlvl1 until xp12 and has logic to re-read the force bolt spellbook (`keep_attack_spell_memorized`) when xp>=10 on dlvl1. But the spellbook is dropped early by item priority; recovering it from the floor depends on finding it again at the right time (no nearby monsters). The deaths clustered at Xp11 (just below the Xp12 gate) suggest the bot fails to maintain reliable ranged offense at the critical phase and falls back to melee against faster/dangerous monsters, leading to deaths before reaching Xp12. Earlier deaths seem unrelated to the spellbook (very low XP, different floors/circumstances) and do not offer an obvious single-function fix without violating the rules.

## What is the problem

Score is mean progress over 15 seeds (parent mean 0.14825). The bottleneck is crossing from Xp11 (0.2548) to Xp12 (0.33265) on dlvl1. Five seeds end at Xp11; getting them to Xp12 would raise the mean. The current strategy depends on force bolt availability at xp>=10+, but the spellbook is not preserved during farming.

## What might solve it

Ensuring the spellbook of force bolt remains available (not dropped) during the relevant farming window on dlvl1 at xp>=10+ makes re-reading the spell more reliable and preserves the intended ranged attack. This is a targeted item retention change that directly supports the existing `keep_attack_spell_memorized` behavior without introducing new rules.
