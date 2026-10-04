# This gameplay

Identity: `wiz-hum-cha-mal`

Read `experiments.md` and edit only the function it names. Do not edit `character.py`, `movement_priority.py`, `exploration_logic.py`, or `global_logic.py`. Do not resubmit the spell parser or the negative ring. Leave the change in the file when you exit. Do not revert it and do not restore the parent. A local game is not the score. A tree that matches the parent is thrown away. Mark the change with a `# hypothesis:` comment. Do not tour the tree. Write that comment and the line in `experiments.md` in ASD-STE100 style. Use one topic in each sentence. Use the active voice and name the actor. Put a condition before the result. Use at most 25 words in a description sentence. Do not use an -ing form. Use one word for one thing. The judge scores the tree after this process exits. Private Dungeons are scored by their verifier after that registration. You do not have those seeds, and a local game is not a private result.

# NetHack 3.6.6

You are editing a bot that plays NetHack 3.6.6 through the NetHack Learning Environment. The public score for this run is `wiz-hum-cha-mal`: a chaotic male human wizard. The same code is later played as every legal character, so a trick that only works for this one character will lose on the private board.

Read `experience.md` and `experiments.md`. Edit only the function that `experiments.md` names. The markdown is not the edit. If the code matches the parent, the gate throws the tree away and nothing is scored. Those two files exist only inside this run. After the code change is in place, add one line to `experiments.md` saying what you changed.

## Goal of the game

Ascend. The bot must get the Amulet of Yendor from Moloch's Sanctum, carry it back up, cross the Elemental Planes, and sacrifice it on the correct high altar on the Astral Plane. Dying, quitting, or sitting still until the turn counter stalls is a loss. The score you are judged on is how far you got, not the in-game points.

## The dungeon

The Dungeons of Doom stair down from the surface. Branches off them: the Gnomish Mines, Sokoban, the Quest, Fort Ludios. Below the main dungeon is Gehennom (mazes, Vlad's Tower, the Wizard of Yendor, the Sanctum). Then the four Elemental Planes and the Astral Plane.

Early death is usually food, a weak melee, a trap, or poison. Later death is usually a wand, a spell, a mind flayer, or a cockatrice. A game that never eats, never heals, or never leaves the first floors cannot score.

## Character

Thirteen roles: Archeologist, Barbarian, Caveman, Healer, Knight, Monk, Priest, Ranger, Rogue, Samurai, Tourist, Valkyrie, Wizard. Five races: human, elf, dwarf, gnome, orc. Three alignments: lawful, neutral, chaotic. Two genders. Valkyrie is female only. That is the 73 identities.

A wizard's strength is spells: damage from a distance, mapping, identification, and later controlled teleport. Mapping and the spell list are not this edit. A wizard's weakness is hit points and melee. Metal body armor blocks spellcasting. Hunger rises when you cast. A chaotic wizard is off the role's natural alignment (neutral), so prayer and sacrifice are less forgiving than for a neutral wizard. Do not assume a starting item you have not seen in the inventory.

Strength, dexterity, constitution, intelligence, wisdom, and charisma are the six stats. Armor class goes down as protection goes up. Energy is the spell budget. Burden from a heavy pack drops speed to zero.

## Items

Weapons, armor, potions, scrolls, wands, spellbooks, rings, amulets, tools. Most are unidentified at first. Price, appearance, and a careful use tell them apart. Useful early finds: food, a healing potion, a wand of striking or magic missile, speed, and any source of magic resistance. Dangerous early uses: an unknown potion or scroll, a wand aimed at yourself, a cockatrice corpse with bare hands.

## Enemies

Early: grid bugs, jackals, rats, goblins, mines inhabitants. They are a damage race the wizard loses in melee if the bot stands and trades hits. Later: liches, mind flayers, demons, the Wizard of Yendor. Elbereth, a door, a corridor, or a ranged spell can keep a fragile character alive. That fact is not this edit. This run edits only the function that `experiments.md` names. A peaceful monster that the bot attacks can ruin the game. A pet that the bot kills is a resource thrown away.

## What a good change looks like

One idea, and it has to be the action `fight2` picks. A number on a heatmap that still loses to the melee action is not a change. Do not edit `exploration_logic.py`, `character.py`, or `movement_priority.py`. Do not edit the spell parser. Leave `_xp_farm_level` in place. Leave `experience_level >= 12` in place. Do not raise it. Do not edit `global_logic.py`. Every other file matches the parent. A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. A game that already lasts about 20,000 turns is not the edit. Seed-specific branches do not count: the private seeds are different games. Restoring the parent is not a result.
