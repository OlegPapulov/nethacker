# This gameplay

Identity: `wiz-hum-cha-mal`

The rules and nuances of the game are in this file.

# NetHack 3.6.6

The public score is `wiz-hum-cha-mal`: a chaotic male human wizard.

Progress is the highest milestone a game reaches. The judge score is the mean of 15 seeds. The score moves when an experience level changes. A longer game at the same level has the same score.

## The task

Your task is to raise the score. You raise it by changing the bot. You use the knowledge in this file.

Make one change. That change is one new function, or one rewrite of one function. The lists below name the actions that raise the score, the actions that lower the score, and the actions that leave the score where it is. Do not repeat a listed action. A listed action is a finished measurement. A listed action covers the measured situation and a similar situation. A similar situation is the same action. Do not rewrite a listed action. When the change you can name is a listed action, leave the bot as it is. You do not know the mean until the judge plays the 15 seeds.

`experience.md` holds the ends of the games the judge already played. Those ends are not the proposal. Do not invent a death that file does not state. An older mean in `experiments.md` is not the current parent.

`experiments.md` holds the one proposal. Propose one change in `experiments.md`, in accordance with these rules. Name the one function you add or the one function you rewrite. Then change the bot from that proposal. Then exit.

Do not revert the change. The judge scores the tree you exit with. A child is kept only when the mean is strictly higher. Do not run `python -m nethackers.arena.run`. The judge plays the 15 seeds after you exit.

## Goal

Ascend. The bot gets the Amulet of Yendor from Moloch's Sanctum. The bot carries the Amulet up. The bot crosses the Elemental Planes. The bot offers the Amulet on the correct high altar on the Astral Plane. Death, a quit, or a stall is a loss. The judge scores how far the bot got.

## The dungeon

The Dungeons of Doom go down from the surface. The branches are the Gnomish Mines, Sokoban, the Quest, and Fort Ludios. Below the main dungeon is Gehennom. Gehennom has mazes, Vlad's Tower, the Wizard of Yendor, and the Sanctum. Then come the four Elemental Planes and the Astral Plane.

An early death is food, a weak melee, a trap, or poison. A later death is a wand, a spell, a mind flayer, or a cockatrice. A game that never eats, never heals, or never leaves the first floors cannot score.

## The first floors

The games that set this score end on the first dungeon levels. The Gnomish Mines, Sokoban, the Quest, Gehennom, and the Planes come after those levels.

Dungeon level 1 holds weak monsters. A lichen, a newt, a grid bug, a jackal, a fox, a goblin, and a sewer rat are typical there. The corpse of one of those monsters is the food. A kitten or a pony on these floors can be peaceful. A bolt trap on these floors throws fire or cold. A rotten corpse on these floors poisons the wizard.

The down stair is the exit after experience level 12. Until then the wizard stays on the floor. The food latch still moves the farm target one level down when the wizard is fainting and no edible corpse is in reach.

The score lists name the action for each of these. When this section and a score list disagree, follow the score list.

## Character

This run is one identity: a chaotic male human wizard. Do not write a branch for another role, race, alignment, or gender.

There are thirteen roles, five races, three alignments, and two genders. Valkyrie is female only. That is 73 identities. The six stats are strength, dexterity, constitution, intelligence, wisdom, and charisma. Armor class goes down as protection goes up. Energy is the spell budget. A heavy pack drops speed to zero. Do not assume an item that you have not seen in the inventory.

A wizard casts spells. That is the advantage. A spell does damage from a distance. The cost is few hit points, hunger when the wizard casts, and spell failure in metal body armor. A learned spell lapses after many turns. Re-reading the force bolt book only while no monster is close raises the score. Reading it while a monster is still nearby lowers the score. Reading that book before the spell is known lowers the score.

A human has no racial intrinsic. An elf has sleep resistance. A dwarf, a gnome, an elf, and an orc have infravision. An orc has poison resistance. This wizard is human, so none of those apply.

This wizard is chaotic. A gift that requires a lawful hero does not apply. The wizard role itself is neutral. That does not change this hero's alignment.

Gender does not change this wizard's spells or hit points.

## Monsters

A monster is an enemy, a pet, or a peaceful creature. The kind changes the action.

- A faster monster takes a turn before the wizard. A few hits kill the wizard. Keep the melee bonus for a faster monster. Giving that bonus to a monster whose speed is above 12, when the name test misses it, leaves the score where it is.
- A weak or slow monster is food more than a threat. A lichen, a newt, and a grid bug are in that group.
- A pet is a resource. Do not attack it. A pet's kill can leave a corpse. Recording that kill leaves the score where it is.
- A peaceful monster is not a target. An attack on one can ruin the game. Stopping a zap on one lowers the score.
- A cockatrice or a chickatrice turns the hero to stone on a touch or a bite. Do not eat that corpse. Do not touch it with bare hands.
- A mind flayer eats the brain. Keep distance. That is a later death.
- A were-creature can give lycanthropy. The new body changes the carrying level. Dropping the pack because the wizard is strained still lowers the score.

## Items

Most items start unidentified. Price, appearance, and one careful use tell them apart.

- A spellbook of force bolt is the ranged attack once the wizard can cast it. The measured cast is in the score lists.
- The wielded weapon is the one the melee roll uses. Skill points in that weapon raise the score. An off-hand weapon does not.
- Metal body armor makes a spell fail more often. The parent already chooses the suit. Swapping that suit for a non-metal suit lowers the score. Armor class still matters.
- A healing potion, a wand of magic missile, or magic resistance is a useful early find. The parent drinks a healing potion below one third of maximum hit points, or below 8 hit points. A potion of speed is a useful find. The parent already chooses when to drink it.
- A ray wand passes through and can bounce. It can hit the wizard. Keep the penalty for that self-hit. Refusing the zap lowers the score.
- A wand of striking is a beam. The beam stops on the first monster or the first door. It does not bounce. It breaks the door. Zapping it as an attack wand lowers the score.
- A corpse is food. Eat before a faint, and only when every monster is too far to walk up during the meal. A longer walk to a corpse lowers the score. A corpse the parent still treats as fresh stays edible.
- An unknown potion, an unknown scroll, or a wand aimed at yourself is a dangerous early use. Do not quaff an unknown potion during a fight.

## Tips

A fight in a doorway lets one monster hit. A fight in a corridor lets one monster hit. An open room lets several monsters hit. Walking toward a doorway while two threats are still at range lowers the score. Writing Elbereth takes the turn. The word helps only on a later turn. When a faster monster can reach the wizard during the writing, the wizard hits, zaps, or steps into a doorway. A seed-specific branch does not count. The private seeds are different games. When a tip and a score list disagree, follow the score list.

## Assumptions

These actions are already measured. The lists below say what raises the score and what lowers the score. Do not repeat a listed action. A listed action covers the measured situation and a similar situation. A similar situation is the same action. A nearby number on a listed action is a similar situation. Leave those actions as they are. Do not rewrite a listed action. When the change you can name is a listed action, leave the bot as it is. Do not revert the change. The judge scores the tree you exit with. You do not know the mean until the judge plays the 15 seeds.

A change that lifts a short game and drops a long game lowers the score. A change that ends every game in the first turns lowers the score to 0.

### These actions raise the score

- Staying on the first dungeon level until experience level 12. The food latch still moves the farm target once, onto dungeon level 2, when the wizard is fainting and no edible corpse is in reach. A further level on that latch lowers the score. The corpse search keeps its current reach.
- Putting skill points into the wielded weapon.
- Casting force bolt from experience level 10, on the first dungeon level, at a monster that is from 2 squares away to 8 squares away. Re-reading that spellbook on the same floor, from experience level 10, only while no monster is close and only after the spell is known.
- Refusing a zap at a floating eye when another monster is within 2 squares. The parent already lowers that zap's priority. A nearby distance on that refusal is the same action.
- During the 50-turn trap window, keeping a hole, a trap door, a fire trap, a magic trap, a teleportation trap, and a level teleporter out of the walk path. The parent already blocks those six. A nearby trap glyph on that block is the same action. A nearby turn count on that window is the same action.

### These actions lower the score

- Changing that force bolt. Casting it before experience level 10, off the first dungeon level, or at an adjacent monster lowers the score. Casting it farther than 8 squares lowers the score. The parent casts it only when the monster is from 2 squares away to 8 squares away. A nearby distance on that far cast is the same action. Keeping less energy before the cast lowers the score. Withholding a throw because the bolt can go down that line lowers the score. Reading the book while a monster is still nearby lowers the score, even when the read is overdue and nothing is adjacent. Reading the book before the spell is known lowers the score. The parent re-reads it only after the spell is known, from experience level 10, on dungeon level 1, when the last read is at least 20,000 turns old. A nearby turn count on that re-read is the same action.
- Learning or casting a second attack spell on dungeon level 1 from experience level 6. A magic missile, a drain life, a chain lightning, a cone of cold, and a fireball are in that group. The parent casts force bolt from experience level 10. A nearby spell name or a nearby experience level on that second cast is the same action.
- Leaving the farm floor while the wizard is only weak. Refusing a down staircase while the wizard is still farming. The stay until experience level 12, and the food latch, stay.
- Moving the food latch past dungeon level 2. The parent latches once, onto level 2, when the wizard is fainting and no edible corpse is in reach. A nearby depth on that extra step is the same action. The one-level latch stays.
- Latching onto dungeon level 2 before the wizard is fainting. The parent latches only when the wizard is fainting and no edible corpse is in reach. A wrapped call inside that test is true before the hunger check runs. A nearby hunger state on that early latch is the same action.
- Dropping the melee bonus for a faster monster. Starting a fight farther than the current reach, on the first floors, while hit points are still high. Stepping toward a doorway because the wizard is hurt or two monsters are adjacent.
- Raising the non-dangerous melee line from 8 hit points to 12. The parent keeps that line at 8. The dangerous line stays at 16. That raise lowers the score. A nearby number on the line at 8 is the same action.
- Lowering the melee priority of a weak monster by 1 when another monster is adjacent. A lichen, a newt, a shrieker, and a grid bug are in that group. The parent does not subtract that point. A nearby penalty on that weak monster is the same action.
- Adding movement points to a doorway or a corridor while two threats are still at range. The parent does not add those points. A nearby distance or a nearby bonus on that walk is the same action.
- Writing Elbereth when hit points are between 45% and 70% of the maximum, an adjacent monster is not a higher level, and a free step is beside the wizard. The parent writes Elbereth when hit points are below 30 and a monster is adjacent. That new window lowers the score. A nearby fraction on that window is the same action.
- Stopping a zap on a peaceful monster, making a zap easier to choose, refusing a zap because the path hits the wizard, or zapping a wand of striking as an attack wand. The parent already subtracts points for a self-hit.
- Waiting longer before a prayer, or praying while hit points are still high enough to fight.
- Praying because the wizard is weak, before fainting. The parent prays for hunger only when the wizard is fainting. That earlier prayer lowers the score. A nearby hunger state on that prayer is the same action.
- Walking farther for a corpse, or eating while a monster can walk up during the meal. The hungry corpse cap stays at 5. Refusing a corpse the parent already treats as fresh lowers the score. The parent already eats that corpse.
- Dropping a carried item when the wizard is strained, overtaxed, or overloaded. The drop runs before the fight, and a corpse goes first. The parent already keeps the pack under its weight budget.
- Swapping a metal body suit for a non-metal suit from experience level 10. Making the metal suit look worse, so a cloth or leather suit wins the slot, lowers the score. A nearby penalty on that suit is the same action. The parent already wears the suit it chose.
- Giving the floating-eye zap penalty to an exploding monster when the wizard is within 2 squares. A gas spore, a yellow light, and a sphere are in that group. A nearby distance or a nearby monster name on that penalty is the same action. The floating-eye penalty stays.
- Quaffing a potion of speed while a monster is visible and hit points are above 6. Quaffing it while hit points are 6 or below, or while no monster is visible, also lowers the score. The parent already chooses when to drink it. A nearby hit-point number on that drink is the same action.
- Drinking a healing potion below half of maximum hit points. The parent drinks below one third, or below 8 hit points. A nearby fraction on that drink is the same action. The line at 8 hit points stays.
- Treating a dwarf, a rothe, or an orc as a dangerous monster. The parent already uses that test for a pet and an insect. A nearby monster name on that test is the same action.
- Putting on a ring or an amulet. Every game ended in the first 14 turns, and the score fell to 0. An unknown ring is included. A nearby accessory on that wear is the same action. The parent leaves rings and amulets in the pack.

### These actions leave the score where it is

- Giving the melee bonus to a monster whose speed is above 12, when the name test misses it. A nearby speed on that bonus is the same action.
- Writing Elbereth while a faster monster is still approaching.
- Praying, or eating a lizard corpse, because the status line shows sickness.
- Searching a smaller area for a corpse while fainting.
- Recording a pet's kill as a corpse, and continuing when a kill message has no vanished glyph.
- Dropping the pet check on a corpse underfoot. The parent skips the freshness stamp while a pet is alive. Dropping that skip leaves the score where it is. A nearby check on that stamp is the same action.
- Keeping only a fire trap and a magic trap out of the walk path. That smaller block leaves the score where it is, during the window and on every call. A nearby depth on that smaller block is the same action. Taking one glyph out of the six-trap window block is that smaller block.
- Raising the hungry corpse walk from 5 squares to 6, or from 5 squares to 10. That cap applies while hunger is below weak. Both changes leave the score where it is. A nearby number on that cap is the same action. The parent keeps the cap at 5.
- Raising the fainting corpse search to 25 squares. The parent keeps that reach at 20. That wider search leaves the score where it is. A nearby number on that reach is the same action.
- Keeping a force bolt spellbook in the pack on depth 1 from experience level 10. The parent already decides which item can drop. That refusal leaves the score where it is. A nearby depth or a nearby experience level on that refusal is the same action.
- Raising the dangerous-monster melee line from 16 hit points to 20. The parent keeps that line at 16. That change leaves the score where it is. A nearby number on that line is the same action.
- Catching an unexpected error and continuing the game. The parent re-raises that error. That catch leaves the score where it is. A nearby error type on that catch is the same action.
- Casting force bolt at a weak monster. A lichen, a newt, a shrieker, and a grid bug are in that group. The parent refuses that cast. That cast leaves the score where it is. A nearby monster name on that cast is the same action.
- Searching or waiting after 150 inactive steps. The parent does not add that guard. That guard leaves the score where it is. A nearby step count on that guard is the same action.
- Raising the force bolt energy wait from 10 to 15. The parent casts when energy is at least 10. That higher wait leaves the score where it is. A nearby energy number on that wait is the same action.

