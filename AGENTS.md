# nethacker

This repo keeps two loops for `wiz-hum-cha-mal`.

The mutator (`mutator/`) edits the bot for the identity given to that run. The test gameplay is `wiz-hum-cha-mal`. `mutator/GAME_RULES.md` is the NetHack rulebook. A run does not start with `experience.md` or `experiments.md`; the loop creates them when they are missing, which is the state before iteration 1. The coding agent rewrites them between iterations. They are gitignored, so they are not in the registered commit and they are not there for the next run.

This folder edits the mutator. Root `GAME_RULES.md` is the competition. Root `experience.md` is the log of mutator runs. Root `experiments.md` is a proposal for the next mutator change.

Do not edit anything under `mutator/` until the user has approved that proposal in chat. Recording a run into the root markdown files is not a mutator edit.

The arena runs in GitHub Actions on `ubuntu-latest` (`linux/amd64`). Do not run `nethackers eval`, `nethackers evolve`, or Docker on the laptop. `.github/workflows/mutate.yml` is the mutator run (`opencode2`, model `opencode/big-pickle`). It registers every scored bot. Private Dungeons are their verifier's queue; registering is the only step this repo can take toward that board. `.github/workflows/score.yml` rescores the tree on `main` when the bot files change.

`NETHACKERS_LOGIN` and `NETHACKERS_TOKEN` are repo secrets. The token is a GitHub user token for `OlegPapulov` (`GET /user` must return that login). It has to still be valid when the job reaches the register step, which can be hours after the run starts. Refresh it just before dispatching a run. `NETHACKERS_GH_TOKEN` is the `gh` token that publishes scored bots. The Actions `GITHUB_TOKEN` cannot call `GET /user`, so `nethackers evolve` treats it as logged out and does not register.

The bot is a directory with `bot.py` (`make_agent()`) and `nethackers.solution.json`. The arena loads `bot.py` at the repo root. AutoAscend is MIT; see `LICENSE`.

Hub reads: `https://nethackers.dunnolab.ai/h/OlegPapulov` and `/programs`. Compare against `/baseline` for `wiz-hum-cha-mal` (AutoAscend's own floor on that identity is about 0.062).

`github.com/dunnolab/nethackers` is private. Install the CLI from PyPI inside the workflow only.
