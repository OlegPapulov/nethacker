# Competition

NetHackers is a public race to write a program that can ascend in NetHack 3.6.6. Ascension is the game's win. Nobody has done it yet.

This repo plays one character, `wiz-hum-cha-mal` (chaotic male human wizard). A submission is one git commit of this tree. The arena loads `bot.py` at the commit root.

## Score

Progression is a number from 0 to 1. It estimates how likely the deepest point the bot reached is to lead to an ascension. An ascension is 1. The reported score is the mean over a batch of games.

AutoAscend's public floor on `wiz-hum-cha-mal` is about 0.062. A run is worth keeping when it beats the bot it started from on that mean.

## How a score is produced

Public Dungeons are 15 published seeds for this identity. `nethackers eval` plays them in the pinned `linux/amd64` arena image. The same seed is a different dungeon on arm64, so the laptop does not score. GitHub Actions does.

`nethackers register` sends that evidence to the hub for this commit. The hub checks that the GitHub account owns the repo, that the commit is public, and that the evidence is the real 15-seed batch from a classified arena image. That is the public leaderboard.

Private Dungeons are 15 secret seeds per character, run by their verifier, not by us. Registering a commit is what puts it in that queue. The verifier takes the least-covered program first, one program at a time, and plays all 73 characters. This repo cannot start that run, choose the seeds, or see per-seed private results. A public registration is the whole of "send this to both boards."

## What this repo is doing

Two loops:

1. The mutator (`mutator/`) edits the bot. It reads a NetHack rulebook and its own notes, makes one change, and those notes are thrown away when the run ends.
2. This folder edits the mutator. `experience.md` records what mutator runs did. `experiments.md` proposes the next change to the mutator. That change is not applied until a human approves it.
