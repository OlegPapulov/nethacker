# The mutator loop — how this repository works

This is the harness for an agent that improves a NetHack bot without human
supervision. It is not documentation of a finished design; it is the design,
written down so the next person changing it knows what they are changing.

## The cycle

One iteration, from `loop/evolve.py`:

1. **Fetch a seed.** The bot to improve, from the hub, a pinned ref, or the
   packaged AutoAscend root.
2. **Score the parent** on the 15 published seeds. This is the baseline every
   later number is compared against.
3. **Compose a brief** (`loop/brief.py`) from the baseline, the identity's
   `experience.md` entries, and `GAME_RULES.md`.
4. **Hand the brief to the mutator agent** in a container, with the tree
   bind-mounted at `/workspace`. The agent edits the bot and leaves a
   `# hypothesis:` comment saying what it expects to improve.
5. **Smoke test**, then **score the child** on the same 15 seeds.
6. **Judge** — `paired_verdict`, then `mean_gate`.
7. **Keep or discard.** A kept tree becomes the next parent, so the run carries
   its own progress forward.
8. **Publish a win.** A `WIN` is pushed to its own branch and registered with
   the leaderboard. Nothing else is published.

Then it repeats, or the run ends. One iteration is 30–90 minutes; most of that
is the agent, not the scoring.

## The two rules that make it work

**A result is only a result if the mean moved.** `paired_verdict` asks whether
most seeds moved forward; `mean_gate` asks whether the batch average improved.
Both must hold for a `WIN`. This is not belt-and-braces — it is the case the
apparatus exists to catch. Run `36615769123` produced 10 seeds forward, cleared
two-thirds *exactly* (`3×10 = 30 ≥ 2×15 = 30`), and scored 0.0374 against a
0.0624 parent. Depth went up; progress went down 40%. The old rule published it.

**Depth is not progress.** `progress` is BALROG progression in [0, 1], and it
rises as the bot survives *and* descends. The mutator agent cannot see the
scorer, so it reconstructs a proxy — usually depth — and optimizes that. In
`36615769123` it flagged the risk itself ("if progression also rewards turns
survived, the change trades 17.5k turns for depth") and was right: the
regression came from survival, exactly as predicted.

## The files

| file | role |
|---|---|
| `loop/evolve.py` | the loop: seed → brief → agent → score → judge → keep |
| `loop/brief.py` | composes the operator's brief; the only channel to the agent |
| `loop/register_evidence.py` | builds the evidence payload `nethackers register` requires |
| `loop/register_winner.py` | pushes a `WIN` and registers it; never raises |
| `loop/build_game_rules.py` | generates `GAME_RULES.md` from the NetHack 3.6.6 source |
| `experience.md` | **written by the agent**, inside the worktree, per iteration |
| `GAME_RULES.md` | game facts parsed from source, scoped to the identity |
| `.github/workflows/our-evolve.yml` | runs the loop in CI, with the auth gate |

Root copies of the `loop/` modules exist and are byte-identical. The workflow
copies them beside `evolve.py` because the agent's imports resolve from there.
**If you edit one, copy it to the other** — a stale root copy imports last
iteration's code and silently does the old thing.

## Why there is no `AGENTS.md` in this repository

`AGENTS.md` looks like the obvious way to instruct the mutator agent, and it is
not. The mutator **strips it**: `harness/refs.py` lists `CLAUDE.md`,
`AGENTS.md`, `.mcp.json`, `opencode.json` and friends in
`_AGENT_CONFIG_NAMES` and passes them to `shutil.ignore_patterns`, so they are
removed from the copy of the tree the agent receives — not hidden, deleted.

The reason is prompt-injection defense. A bot tree is fetched from the
leaderboard, and if any published tree could carry its own `AGENTS.md`, a
malicious submission could hand the mutator instructions and hijack the loop.
The list is applied to every copy that feeds the agent, worktree and `/refs/`
alike, so there is no supported way around it.

**The brief is the channel.** `ContainerOperator.run(brief=...)` takes a string
and the mutator does not care where it came from, so `loop/brief.py` composes it
and everything the agent must know travels in that one string. `SCORING`,
`HOWTO` and `CONTRACT` in `brief.py` are the agent's standing instructions,
and they are maintained there rather than in a file the agent would ignore.

`GAME_RULES.md` and `experience.md` *do* survive into the worktree, and the
agent can read them. Verified against `_mutator_ignore` — they pass, while
`AGENTS.md` and `opencode.json` do not.

## `experience.md` is the memory, and the tree is what carries it

The agent writes its own entries, following the template in the brief, into
`/workspace/experience.md` during the iteration. Because the parent is
`shutil.copytree`'d into the next worktree, and a kept winner becomes the next
parent, **the log travels with the bot automatically**. A `KEEP` carries its
written experience forward; a discarded mutant takes its log with it.

This is why the log lives in the worktree and not in the repository root: the
repository holds the harness, the worktree holds the state. Keeping the log in
the repo would require a separate mechanism to decide which iteration's log
belongs to which parent, and the copytree already answers that.

## Running it

```bash
gh workflow run our-evolve.yml -f identity=wiz-hum-cha-mal -f iterations=1
```

Registration is opt-in by credential. Add two repository secrets:

- `NETHACKERS_TOKEN` — a **classic** PAT, scope `public_repo`, no expiry
- `NETHACKERS_LOGIN` — the login it belongs to

`nethackers whoami` gates it before an iteration is spent, so a bad token
degrades to "keeps trees, publishes nothing" instead of silently discarding
every candidate. Do **not** paste the `access_token` from `nethackers login`:
it expires in about eight hours, and `write_credentials.py` records no expiry,
so the CLI would treat a dead token as permanent and never refresh it.

## What the metric will not tell you

Fifteen seeds is a noise floor, not a sample. Measured SE is 0.0085 on this
identity, and one seed can swing 0.18. A change of 0.01 is not resolvable at
this batch size, which is why a `WIN` needs the per-seed shape *and* a moved
mean *and* is easy to lose by a mechanism that is real but small. The mutator
agent's own response to this — measuring on held-out seeds it did not tune
against — is the right instinct, and the harness does not yet do it
automatically.
