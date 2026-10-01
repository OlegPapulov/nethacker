# nethacker

AutoAscend, scored on NetHackers as `wiz-hum-cha-mal`.

The arena runs on a GitHub-hosted `linux/amd64` runner. Pushing `bot.py` or `autoascend/` starts [score.yml](.github/workflows/score.yml), which evaluates the published 15-seed batch and registers this commit with the hub.

AutoAscend is MIT, Copyright © 2022 Maciej Sypetkowski, Michał Sypetkowski. See [LICENSE](LICENSE). `bot.py` and `arena_adapter.py` are the NetHackers arena shim (Apache-2.0, from the `nethackers` package).
