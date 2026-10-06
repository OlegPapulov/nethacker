# This gameplay

Identity: `wiz-hum-cha-mal`

You develop a bot to play NetHack 3.6.6. The rules and nuances of the game are in this file. Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. The mean falls when a long game loses a milestone, even when a short game lasts longer. Describe the games in `experience.md`. Propose the change in `experiments.md`. Change the bot from that proposal. Do not run `python -m nethackers.arena.run`. The judge plays the 15 seeds after you exit.

# NetHack 3.6.6

You edit a bot that plays NetHack 3.6.6. The public score is `wiz-hum-cha-mal`: a chaotic male human wizard. The same code later plays every legal character. A trick that works for only this character loses on the private board.

Read `experience.md` and `experiments.md`. Describe the games in `experience.md`. Propose one change in `experiments.md`. Change the bot from that proposal. When the code matches the parent, the gate throws the tree away.

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

These facts explain a death. They are not a second edit. Propose one change in `experiments.md`.

- A fight in a doorway lets one monster hit. A fight in a corridor lets one monster hit. An open room lets several monsters hit.
- Elbereth on the floor makes this bot wait. Melee, ranged, and zap then lose priority. A long game gets shorter.
- A faster monster takes a turn before the wizard takes a turn. A few hits kill the wizard.
- A pet is a resource. An attack on a peaceful monster can ruin the game.
- Eat before a faint. A faint next to a monster is a death.
- A prayer can feed the wizard. A god that rejects the prayer takes an experience level and hit points.
- A cockatrice corpse turns the hero to stone. Do not eat it. Do not touch it with bare hands.
- Do not quaff an unknown potion during a fight.
- A seed-specific branch does not count. The private seeds are different games.

## What a good change looks like

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. Experience level moves that score. The mean falls when a long game loses a milestone, even when a short game lasts longer. A down stair is not, by itself, progress.

Leave the corpse walk capped at 20 squares. Leave `experience_level >= 12` in place. Leave the fainting test that sets `_xp_farm_level` to 2 as it is. Do not edit `fight_heur.py`, `exploration_logic.py`, `fight2`, or `emergency_strategy`.

Describe the games in `experience.md`. Propose one change in `experiments.md`. Change the bot from that proposal. Do not run a local game. The judge plays the seeds after you exit.
