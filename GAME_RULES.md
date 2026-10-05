# This gameplay

Identity: `wiz-hum-cha-mal`

Read `experiments.md` and edit only the function it names. The file you may change is the file that contains that function. Every other file matches the parent. Do not edit `fight_heur.py`, `character.py`, `movement_priority.py`, `exploration_logic.py`, or `global_logic.py`. Do not resubmit the spell parser or the negative ring. Leave the change in the file when you exit. Do not revert it and do not restore the parent. Do not run `python -m nethackers.arena.run`. Do not wait on a local game. The judge plays the 15 seeds after you exit. A local game is not the score. The score is the mean of those seeds. A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. A tree that matches the parent is thrown away. Mark the change with a `# hypothesis:` comment in ASD-STE100 style. Use one topic in each sentence. Use the active voice and name the actor. Put a condition before the result. Use at most 25 words. Do not use an -ing form.

# NetHack 3.6.6

You edit a bot that plays NetHack 3.6.6. The public score is `wiz-hum-cha-mal`: a chaotic male human wizard. The same code later plays every legal character. A trick that works for only this character loses on the private board.

Read `experience.md` and `experiments.md`. Edit only the function that `experiments.md` names. The markdown is not the edit. When the code matches the parent, the gate throws the tree away. After the code change is in place, add one line to `experiments.md`. Say what you changed.

## Goal

Ascend. The bot gets the Amulet of Yendor from Moloch's Sanctum. The bot carries the Amulet up. The bot crosses the Elemental Planes. The bot offers the Amulet on the correct high altar on the Astral Plane. Death, a quit, or a stall is a loss. The judge scores how far the bot got.

## The dungeon

The Dungeons of Doom go down from the surface. The branches are the Gnomish Mines, Sokoban, the Quest, and Fort Ludios. Below the main dungeon is Gehennom. Gehennom has mazes, Vlad's Tower, the Wizard of Yendor, and the Sanctum. Then come the four Elemental Planes and the Astral Plane.

An early death is food, a weak melee, a trap, or poison. A later death is a wand, a spell, a mind flayer, or a cockatrice. A game that never eats, never heals, or never leaves the first floors cannot score.

## Character

There are thirteen roles. There are five races: human, elf, dwarf, gnome, and orc. There are three alignments: lawful, neutral, and chaotic. There are two genders. Valkyrie is female only. That is 73 identities.

A wizard casts spells. A spell does damage from a distance. Metal body armor blocks a spell. Hunger rises when the wizard casts. Mapping and the spell list are not this edit.

A wizard has few hit points. A wizard loses a melee when the bot stands and trades hits. The wizard role is neutral. This wizard is chaotic, so prayer is less safe than for a neutral wizard. Do not assume an item that you have not seen in the inventory.

The six stats are strength, dexterity, constitution, intelligence, wisdom, and charisma. Armor class goes down as protection goes up. Energy is the spell budget. A heavy pack drops speed to zero.

## Items

Most items start unidentified. Price, appearance, and one careful use tell them apart. A useful early find is food, a healing potion, a wand of striking, a wand of magic missile, speed, or magic resistance. A dangerous early use is an unknown potion, an unknown scroll, a wand aimed at yourself, or a cockatrice corpse.

## Tips

These facts explain a death. They are not a second edit. Edit only the function that `experiments.md` names.

- A fight in a doorway lets one monster hit. A fight in a corridor lets one monster hit. An open room lets several monsters hit.
- Elbereth on the floor stops many monsters. Some monsters still attack.
- A faster monster takes a turn before the wizard takes a turn. A few hits kill the wizard.
- A pet is a resource. An attack on a peaceful monster can ruin the game.
- Eat before a faint. A faint next to a monster is a death.
- A prayer can feed the wizard. A god that rejects the prayer takes an experience level and hit points.
- A cockatrice corpse turns the hero to stone. Do not eat it. Do not touch it with bare hands.
- Do not quaff an unknown potion during a fight.
- A seed-specific branch does not count. The private seeds are different games.

## What a good change looks like

One change. The change is the function that `experiments.md` names. That function is `emergency_strategy`. The file you may change is `agent.py`. Every other file matches the parent.

The score is the mean of the 15 judge seeds. A game under 10,000 turns that lasts longer raises the mean. A long game that gets shorter lowers the mean. A local game is not the score.

Do not edit `fight_heur.py`, `exploration_logic.py`, `character.py`, `movement_priority.py`, or `global_logic.py`. Do not edit the spell parser. Do not resubmit the negative ring.

Leave `_xp_farm_level` in place. Leave `experience_level >= 12` in place. Do not raise it. Do not remove the comment marks on the Elbereth block. That block rests for 8 turns. Do not call `direction('.')`. Do not run a local game. The judge plays the seeds after you exit.
