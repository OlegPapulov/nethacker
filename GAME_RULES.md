# This gameplay

Identity: `wiz-hum-cha-mal`

The rules and nuances of the game are in this file.

# NetHack 3.6.6

The public score is `wiz-hum-cha-mal`: a chaotic male human wizard.

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. The score moves when an experience level changes. A longer game at the same level has the same score.

## The task

Your task is to raise the score. You raise it by changing the bot. You use the knowledge in this file.

Make one change. That change is one new function, or one rewrite of one function. The lists below name the actions that lower the score and the actions that leave the score where it is. Do not repeat a listed action. The one change raises the score. It does not lower the score.

`experience.md` holds the ends of the games the judge already played. Read it. Describe why the bot lost. Do not invent a death that file does not state.

`experiments.md` holds the one proposal. Propose one change in `experiments.md`, in accordance with these rules. Name the one function you add or the one function you rewrite. Then change the bot from that proposal. Then exit.

Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result. A child is kept only when the mean is strictly higher. Do not run `python -m nethackers.arena.run`. The judge plays the 15 seeds after you exit.

## Goal

Ascend. The bot gets the Amulet of Yendor from Moloch's Sanctum. The bot carries the Amulet up. The bot crosses the Elemental Planes. The bot offers the Amulet on the correct high altar on the Astral Plane. Death, a quit, or a stall is a loss. The judge scores how far the bot got.

## The dungeon

The Dungeons of Doom go down from the surface. The branches are the Gnomish Mines, Sokoban, the Quest, and Fort Ludios. Below the main dungeon is Gehennom. Gehennom has mazes, Vlad's Tower, the Wizard of Yendor, and the Sanctum. Then come the four Elemental Planes and the Astral Plane.

An early death is food, a weak melee, a trap, or poison. A later death is a wand, a spell, a mind flayer, or a cockatrice. A game that never eats, never heals, or never leaves the first floors cannot score.

## Character

There are thirteen roles. There are five races: human, elf, dwarf, gnome, and orc. There are three alignments: lawful, neutral, and chaotic. There are two genders. Valkyrie is female only. That is 73 identities.

A wizard casts spells. A spell does damage from a distance. Metal body armor blocks a spell. Hunger rises when the wizard casts. Mapping and the spell list are not this edit.

A wizard has few hit points. The wizard role is neutral. This wizard is chaotic. Do not assume an item that you have not seen in the inventory.

The six stats are strength, dexterity, constitution, intelligence, wisdom, and charisma. Armor class goes down as protection goes up. Energy is the spell budget. A heavy pack drops speed to zero.

## Items

Most items start unidentified. Price, appearance, and one careful use tell them apart. A useful early find is food, a healing potion, a wand of magic missile, speed, or magic resistance. A wand of striking is a beam. The beam stops on the first monster or the first door. It does not bounce. It breaks the door. A ray passes through and can bounce. Force bolt is the ranged attack once the wizard can cast it. A dangerous early use is an unknown potion, an unknown scroll, a wand aimed at yourself, or a cockatrice corpse.

## Tips

These facts explain a death.

- A fight in a doorway lets one monster hit. A fight in a corridor lets one monster hit. An open room lets several monsters hit.
- A faster monster takes a turn before the wizard takes a turn. A few hits kill the wizard.
- A pet is a resource. An attack on a peaceful monster can ruin the game.
- Eat before a faint. A faint next to a monster is a death. Start a meal only when every monster is too far to walk up during the meal. A monster a few squares away still holds the turn.
- Writing Elbereth takes the turn. The word helps only on a later turn, after it is on the floor. When a faster monster can reach the wizard during the writing, the wizard hits, zaps, or steps into a doorway.
- A cockatrice corpse turns the hero to stone. Do not eat it. Do not touch it with bare hands.
- Do not quaff an unknown potion during a fight.
- A seed-specific branch does not count. The private seeds are different games.

## Assumptions

These actions are already measured. The lists below say what raises the score and what lowers the score. Do not repeat a listed action. A nearby number on a listed action is the same action. Leave those actions as they are. Do not revert the change. The judge scores the tree you exit with. A tree that matches the parent is not a result.

A change that lifts a short game and drops a long game lowers the score.

### These actions raise the score

- Staying on the first dungeon level until experience level 12.
- Putting skill points into the wielded weapon.
- Casting force bolt from experience level 10, on the first dungeon level, at a monster that is not adjacent.
- When the wizard is fainting and no edible corpse is in reach, moving the farm target one level down. The corpse search keeps its current reach.

### These actions lower the score

- Casting force bolt before experience level 10.
- Casting force bolt off the first dungeon level.
- Casting force bolt at an adjacent monster. A higher priority on that cast is the same action.
- Keeping less energy before that cast.
- Waiting longer before a prayer.
- Praying while hit points are still high enough to fight.
- Walking farther for a corpse.
- Eating while a monster can walk up during the meal.
- Dropping the melee bonus for a faster monster.
- Leaving the farm floor while the wizard is only weak.
- Stopping a zap on a peaceful monster.
- Making a zap easier to choose.
- Stepping toward a doorway because the wizard is hurt or two monsters are adjacent.
- Zapping a wand of striking as an attack wand.
- Refusing a corpse underfoot that the parent still treats as fresh.
- Dropping a carried item when the wizard is strained, overtaxed, or overloaded. The drop runs before the fight, and a corpse goes first. The parent already keeps the pack under its weight budget.

### These actions leave the score where it is

- Writing Elbereth while a faster monster is still approaching.
- Praying, or eating a lizard corpse, because the status line shows sickness.
- Searching a smaller area for a corpse while fainting.

