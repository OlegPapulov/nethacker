# NetHack 3.6.6

The public score is `wiz-hum-cha-mal`: a chaotic male human wizard.

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds.

Describe the games in `experience.md`. Propose one change in `experiments.md`. Change the bot from that proposal.

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

Most items start unidentified. Price, appearance, and one careful use tell them apart. A useful early find is food, a healing potion, a wand of striking, a wand of magic missile, speed, or magic resistance. A dangerous early use is an unknown potion, an unknown scroll, a wand aimed at yourself, or a cockatrice corpse.

## Tips

These facts explain a death.

- A fight in a doorway lets one monster hit. A fight in a corridor lets one monster hit. An open room lets several monsters hit.
- A faster monster takes a turn before the wizard takes a turn. A few hits kill the wizard.
- A pet is a resource. An attack on a peaceful monster can ruin the game.
- Eat before a faint. A faint next to a monster is a death. Start a meal only when every monster is too far to walk up during the meal. A monster a few squares away still holds the turn.
- Writing Elbereth takes the turn. The word helps after it is on the floor. An adjacent monster still acts while you write. When hit points are low, hit, zap, or step into a doorway.
- A cockatrice corpse turns the hero to stone. Do not eat it. Do not touch it with bare hands.
- Do not quaff an unknown potion during a fight.
- A seed-specific branch does not count. The private seeds are different games.

## Assumptions

These changes are already measured. Do not repeat a listed change. A nearby number on a listed test is the same change. The next edit is one existing test that this list does not name. An unchanged bot leaves the mean at 0.114.

- A prayer wait of 3,500 turns drops the mean from 0.114 to 0.024. Every seed at 0.179 or above falls. Seed 9 falls from 0.255 to 0.018. The parent wait is 500 turns at low hit points and 400 turns while fainting. The parent also prays below 6 hit points. Raising that 6 to 9 drops the mean from 0.114 to 0.074. Seed 9 falls from 0.255 to 0.000 in 702 turns. A nearby number in that same test is the same change.
- A corpse walk longer than 20 squares drops the mean. A cap of 30 drops it to 0.107, and seeds 5 and 6 fall from 0.179 to 0.037. A cap of 25 drops it to 0.107, and seed 13 falls from 0.179 to 0.051. The walk that holds the current mean stops at 20 squares. The fainting latch uses that same 20-square search. Cutting it to 10 squares leaves the mean at 0.114. All 15 seeds keep the parent turn counts. A nearby distance on that search is the same change.
- The parent melee bonus is +15 when hit points are above 8 or the monster is faster. Replacing the faster-monster test with a fatal-melee test drops the mean from 0.114 to 0.105. Seed 3 falls from 0.179 to 0.029.
- The parent sets the farm level to 2 when hunger is fainting and no edible corpse is in reach. Also setting that level when hunger is weak and experience level is at least 10 leaves the mean at 0.114. Seed 9 stays at 0.255. Seeds 1, 3, 5, and 6 stay at 0.179. The mean of turns falls from 36,648 to 34,898. Seed 6 falls from 73,840 turns to 54,297 turns. A nearby experience level or a nearby hunger state in that same test is the same change.
- The parent lets the wizard eat when every monster is more than 7 squares away. When hunger is weak, letting a monster at 5 or 6 squares through drops the mean from 0.114 to 0.082. Seed 9 falls from 0.255 to 0.051. A nearby distance in that same test is the same change.
- The parent wand path stops on a pet. Treating a peaceful monster as that same stop drops the mean from 0.114 to 0.098. Seed 9 falls from 0.255 to 0.117. Seed 0 falls from 0.117 to 0.075. Seed 3 falls from 0.179 to 0.117. That same stop on a peaceful monster is the same change.

## The edit

Change one test that already exists. Do not add a new action. Describe the games in `experience.md`. Propose one change in `experiments.md`, in accordance with these rules. Change the bot from that proposal. Do not run `python -m nethackers.arena.run`. The judge plays the 15 seeds after you exit.
