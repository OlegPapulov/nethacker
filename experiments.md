# Next mutator experiment

Applied. The instruction no longer asks for an Elbereth write. Seed 4 must last longer, and seed 3 and seed 9 must keep their progress.

## Why it stopped

Run 37331933484 scored 0.10213461846666004. The parent is 0.11444300565928403. The mean falls by 0.012.

## What is the problem

The operator followed the safe test. The write runs when depth is 1, hit points are below 6, and no monster is adjacent. The rest loop stays commented.

Seed 4 rose from Xp:2 to Xp:7. Seed 8 rose from Xp:6 to Xp:8. Seed 3 fell from Xp:10 to Xp:5. Seed 13 fell from Xp:10 to Xp:8. The losses are larger than the gains.

The word changes the next fight. `wait_action` returns about 30 when the floor says Elbereth. Melee, ranged, and zap each lose 100. The bot stands on the word and stops the attacks that used to raise the long games.

## What might solve it

The culprit is the wait after the word is written. `wait_action` then outranks melee in every game that reaches that square. Seed 4 and seed 3 share that code.

The shortest parent game is seed 4, at 2,742 turns and Xp:2. A longer seed 4 raises the mean only when the long games keep their progress. The last two writes lengthened seed 4 and shortened seed 3. Seeds 10 and 12 stayed at Xp:4 and Xp:5.

Do not tell the operator to edit only for the shortest run. The judge still scores all 15 seeds, and the edit is one function. Do not send another Elbereth write.

Leave `fight_heur.py` forbidden. Leave the level-12 gate, the food latch, and the corpse cap. Leave the commented rest loop in place.

## Result

- iteration 1: 0.102 not kept (no-cell-improved). Decreases the mean by 0.012 (from 0.114 to 0.102). Seed 4 rose from 0.018 to 0.051. Seed 8 rose from 0.037 to 0.075. Seed 3 fell from 0.179 to 0.029. Seed 13 fell from 0.179 to 0.075.
