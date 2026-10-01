# nethacker

This repo is the AutoAscend baseline submitted to NetHackers for one identity: `wiz-hum-cha-mal`.

The arena runs in GitHub Actions on `ubuntu-latest` (`linux/amd64`). Do not run `nethackers eval` or Docker on the laptop. A push that changes `bot.py`, `arena_adapter.py`, `autoascend/`, or `nethackers.solution.json` starts `.github/workflows/score.yml`. That workflow evaluates the identity's 15 published seeds and registers this commit with the hub.

`NETHACKERS_LOGIN` and `NETHACKERS_TOKEN` are repo secrets. The token is a GitHub user token for `OlegPapulov` (`GET /user` must return that login). It has to still be valid when the job reaches the register step, which can be hours after the run starts. Refresh it just before dispatching a run.

The bot is a directory with `bot.py` (`make_agent()`) and `nethackers.solution.json`. The arena loads `bot.py` at the repo root. AutoAscend is MIT; see `LICENSE`.

Hub reads: `https://nethackers.dunnolab.ai/h/OlegPapulov` and `/programs`. Compare against `/baseline` for `wiz-hum-cha-mal` (AutoAscend's own floor on that identity is about 0.062).

`github.com/dunnolab/nethackers` is private. Install the CLI from PyPI inside the workflow only.
