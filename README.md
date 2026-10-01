# nethacker

AutoAscend for `wiz-hum-cha-mal`, plus a mutator that edits it.

`GAME_RULES.md` here is the competition. `mutator/GAME_RULES.md` is NetHack. The mutator run is [mutate.yml](.github/workflows/mutate.yml): OpenCode `opencode/big-pickle`, one bot experiment per iteration, every scored bot registered. Its playthrough notes are thrown away at the end of the run. A change to the mutator itself waits for a human yes.

AutoAscend is MIT, Copyright © 2022 Maciej Sypetkowski, Michał Sypetkowski. See [LICENSE](LICENSE). `bot.py` and `arena_adapter.py` are the NetHackers arena shim (Apache-2.0, from the `nethackers` package).
