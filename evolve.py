"""Our loop: pull an elite, measure it, brief the operator, keep a winner.

The stock `nethackers evolve` is autonomous and its brief carries only scores,
so nothing this project has measured can reach the operator. This loop is the
same shape with one difference: **we compose the brief** from `experience.md`
and the baseline diagnosis, and hand that string to the project's mutator.

The mutator, the arena, the gate and the archive are all reused unchanged --
they are the parts that know about NetHack. Only the brief is ours.

    pull elite -> score it (published batch) -> build our brief
      -> operator edits the tree in the mutator
        -> smoke gate -> confirm on the published batch
          -> paired per-seed verdict -> keep or discard

The verdict is deliberately stricter than the project's, and the reason is in
`SCORING` in brief.py: progression takes ~5 distinct values across 15 seeds and
one seed can swing 0.18, so a positive mean is not evidence. We require most
seeds to improve.

Usage:
    evolve.py <identity> --iterations 2 --operator opencode2 \\
        --model opencode/big-pickle [--seed-mode pinned|hub|autoascend]
"""

from __future__ import annotations

import argparse
import datetime
import difflib
import json
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
import threading
from pathlib import Path

def _find_repo_root(start: Path) -> Path:
    """The directory holding the loop sources.

    See the same function in brief.py for why this searches upward and stops
    before the filesystem root. Running from the repository root rather than
    from loop/ was the difference between an 8,000-character brief and a
    3,600-character one that silently contained none of the notes.
    """
    for candidate in [start, *start.parents]:
        if candidate.parent == candidate:
            break
        if (candidate / "loop" / "evolve.py").is_file():
            return candidate
    return start.parent


REPO_ROOT = _find_repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(__file__).resolve().parent))

import brief as brief_mod  # noqa: E402
import register_winner as publish_mod  # noqa: E402

ARENA_IMAGE = (
    "ghcr.io/dunnolab/nethackers-arena@sha256:"
    "0d0b0e779ebda4a05b5a22b39cfafcd2d2d9ef739ea60d9aae79052d55c767ae"
)
MUTATOR_IMAGE = (
    "ghcr.io/dunnolab/nethackers-mutator@sha256:"
    "32c9222455b2f62082540a9f7293aa8fafc2bd5cb9ba7f4553fe79593706bee5"
)

#: Seeds kept for the paired comparison, from the arena's published batch.
PUBLISHED_SEEDS = 15

#: Concurrent arena episodes per score(). Sized for the CI runner
#: (`ubuntu-latest`, 4 vCPU): the agent container has exited by the time either
#: score runs, so scoring may use the whole machine.
#:
#: Not `None`, which the CLI documents as "one per CPU the container runtime
#: has": `evaluate` threads the value straight through to `run_prepared`, which
#: computes `max(1, min(max_parallel_evals, n))`, and `min(None, 15)` raises
#: TypeError. The package's own default is unusable on this path, so the cap is
#: an explicit int.
EVAL_PARALLELISM = 4

#: Hard wall-clock ceiling on one agent turn. The agent gets a budget, not a
#: blank cheque: run 36710578461 spent 81.3 min in the agent (56.0 of it asleep
#: in `sleep`), and under a 360-minute job cap a single runaway turn can push
#: the rest of the iteration out of existence. Capping the turn means a
#: confused agent costs one iteration rather than the run. The brief now also
#: says how to measure cheaply, so this is a backstop, not the normal path.
AGENT_TIMEOUT_SECONDS = 40 * 60

#: One cheap episode on a reserved seed, to reject a mutant that does not run.
SMOKE_SEED = 9000
SMOKE_STEPS = 2000

#: A win needs most seeds forward, and a floor in absolute terms. A 4-up-3-down
#: split is a coin flip under a sign test, so it is not a win.
MIN_SEEDS_FORWARD = 5
MIN_TWO_THIRDS = True

#: ...and the batch mean has to move up as well. The per-seed test asks a
#: per-seed question, and it can be cleared by a handful of large swings while
#: the average stays flat or falls. The mean is the number the leaderboard ranks
#: on, so a result that did not move it is not a result.
#:
#: Strictly greater, no significance margin. With 15 seeds the measured SE is
#: 0.0085, so a mean that improved by 0.001 is inside the noise band; this gate
#: catches a result that is flat or negative, not one that is small. Asking for
#: every one of the 15 seeds to improve is not a stricter version of this -- it
#: is an unreachable one, because a seed is a whole stochastic game and a
#: one-line change diverges the entire trajectory (per-seed SD is 0.033).
MEAN_MUST_IMPROVE = True

#: Verdicts that make a mutant the next parent. Only WIN is a result anybody can
#: register; KEEP is a better starting point to keep searching from, and nothing
#: more. Keeping the two apart is the point -- see `paired_verdict`.
KEEPING_VERDICTS = ("WIN", "KEEP")


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def spec_for(identity: str, seeds: int = PUBLISHED_SEEDS, max_steps: int | None = None):
    from nethackers.contracts.models import ObjectiveSpec
    from nethackers.hub.objectives import CATALOG

    dev = CATALOG[identity]
    return ObjectiveSpec(
        name=f"{identity}__ours",
        kind="identity",
        batch=tuple((s, identity) for s in range(seeds)),
        max_steps=max_steps or dev.max_steps,
        no_progress_timeout=dev.no_progress_timeout,
        action_timeout_seconds=dev.action_timeout_seconds,
        aggregation=dev.aggregation,
    )


def score(tree: Path, identity: str, *, seeds: int = PUBLISHED_SEEDS, max_steps=None):
    """Score `tree` on `identity`'s published batch.

    Returns `(mean, results, raw)`, and the third element is not redundant.
    `results` is the loop's own narrow projection -- the paired arithmetic in
    `paired_verdict` reads `seed`/`depth`/`death` and nothing else. `raw` is the
    untouched `EpisodeResult.__dict__`, which is what `nethackers register`
    reads: the hub looks up `trajectory_id`, `max_depth`, `cause_of_death` and
    `ascended` by name, so the projection would hand it episodes it cannot
    resolve. One evaluation, two shapes; re-scoring to recover `raw` would mean
    trusting a second sample of a batch with a per-seed SD of 0.033.

    Episodes run `EVAL_PARALLELISM` at a time. This used to be pinned to 1,
    which cost ~6.4 min per score and therefore ~13 min per iteration for
    nothing: `run_prepared` keys results by spec index (`results[i] = result`
    after `as_completed`) and returns them in `specs` order, so the worker
    count cannot reach the result. Verified by driving `run_prepared` with a
    stub `run_one` and deliberately uneven episode costs at 1/2/4/8 workers:
    identical per-seed values and an identical mean every time, still in specs
    order. The score is a pure function of (tree, identity, seeds); parallelism
    is schedule-only.
    """
    from nethackers.harness import evaluate as E

    mean, evidence = E.evaluate(
        str(tree), spec_for(identity, seeds, max_steps), ARENA_IMAGE,
        now=now(), runtime="docker", max_parallel_evals=EVAL_PARALLELISM,
    )
    results = [
        {
            "seed": r.trajectory_id, "turns": r.turns, "depth": r.max_depth,
            "progress": r.progress, "death": r.cause_of_death, "status": r.status,
        }
        for r in evidence.results
    ]
    return mean, results, [r.__dict__ for r in evidence.results]


def mean_gate(child_mean: float, parent_mean: float, verdict: dict) -> dict:
    """Demote a WIN whose batch mean did not actually improve.

    `paired_verdict` and this answer different questions, and the loop needs
    both answered. The paired test asks whether the mutation moved most seeds
    forward; the mean test asks whether the batch as a whole got better. A
    mutant can clear the first while losing the second -- several seeds jumping
    far enough to outrun the ones that slipped -- and the result is registered
    against the board on a number that went down.

    A demotion lands on KEEP, not on a discard. The seeds really did move
    forward, so the tree is still a better place to search from; it just is not
    a better bot, and `history.json` records which of the two it was.
    """
    if not MEAN_MUST_IMPROVE or verdict["verdict"] != "WIN":
        return verdict
    if child_mean > parent_mean + 1e-9:
        return verdict
    return {
        **verdict,
        "verdict": "KEEP",
        "why": (
            f"{verdict['why']}, but the mean did not improve "
            f"({child_mean:.4f} vs {parent_mean:.4f}) -- kept as the parent, "
            f"not a publishable win"
        ),
    }


def paired_verdict(child: list[dict], parent: list[dict]) -> dict:
    """Judge a mutant against its parent, per seed, on identical seeds.

    Three verdicts, not two. The loop was losing real progress by collapsing
    "not good enough to publish" into "discard": the 15-seed batch has a
    per-seed SD of 0.033, so a single mechanism worth +0.005 cannot clear a
    five-seed bar however real it is. The agent measuring this identity put it
    plainly -- 15 seeds gives SE 0.0085, 90 gives 0.0054, and every mechanism
    it found had an expected effect under 0.01. Under the old rule that work
    could only ever come back as a dead end.

    So a child that moves seeds forward without being a net regression is
    KEPT: it becomes the next parent, and the search continues from it. It is
    not a WIN, it is not publishable, and `history.json` says which it was.
    Only a child that clears both the absolute and the two-thirds bar is a
    result, and a child that moves nothing at all is still thrown away -- there
    is nothing to keep when the tree came back identical.
    """
    child_by = {r["seed"]: r for r in child}
    parent_by = {r["seed"]: r for r in parent}
    shared = sorted(set(child_by) & set(parent_by))
    if not shared:
        return {"verdict": "NO-BASELINE", "why": "no shared seeds"}

    def moved(s):
        a, b = child_by[s], parent_by[s]
        return (
            abs(a["progress"] - b["progress"]) > 1e-9
            or a["turns"] != b["turns"]
            or a["depth"] != b["depth"]
        )

    def forward(s):
        a, b = child_by[s], parent_by[s]
        return (
            a["progress"] > b["progress"] + 1e-9
            or a["depth"] > b["depth"]
            or (a["depth"] == b["depth"] and a["turns"] > b["turns"])
        )

    changed = [s for s in shared if moved(s)]
    up = [s for s in changed if forward(s)]
    down = [s for s in changed if not forward(s)]
    deeper = [s for s in shared if child_by[s]["depth"] > parent_by[s]["depth"]]

    # Both bars, not either: MIN_SEEDS_FORWARD is the floor in absolute terms
    # and MIN_TWO_THIRDS is the shape of the split that earned them.
    confirmed = len(up) >= MIN_SEEDS_FORWARD and (
        not MIN_TWO_THIRDS or 3 * len(up) >= 2 * len(changed)
    )

    if not changed:
        verdict, why = "NOT-A-WIN", "no seed moved on any signal"
    elif confirmed:
        verdict, why = "WIN", f"{len(up)} forward, {len(down)} back, {len(deeper)} deeper"
    elif len(up) > len(down):
        verdict, why = "KEEP", (
            f"not a regression: {len(up)} forward against {len(down)} back, but "
            f"short of the {MIN_SEEDS_FORWARD}-seed bar -- kept as the parent, "
            f"not a publishable win"
        )
    elif len(up) < MIN_SEEDS_FORWARD:
        verdict, why = "NOT-A-WIN", (
            f"only {len(up)} seed(s) moved forward, below the {MIN_SEEDS_FORWARD} "
            f"required ({len(down)} went back)"
        )
    else:
        verdict, why = "NOT-A-WIN", (
            f"{len(up)} of {len(changed)} moved seeds went forward, short of "
            f"two-thirds ({len(down)} went back)"
        )

    return {
        "verdict": verdict, "why": why, "shared_seeds": len(shared),
        "changed": changed, "forward": up, "backward": down, "deeper": deeper,
    }


def fetch_seed(identity: str, mode: str, reference: str | None) -> Path:
    target = Path("seed-bot")
    if mode == "autoascend":
        import nethackers
        packaged = Path(nethackers.__file__).parent / "roots" / "autoascend"
        shutil.copytree(packaged, target)
    elif mode == "pinned" and reference:
        subprocess.run(["nethackers", "pull", reference, str(target)], check=True)
    else:
        elites = json.loads(
            subprocess.run(
                ["nethackers", "elites", "--scope", identity],
                capture_output=True, text=True, check=True,
            ).stdout
        )
        rows = [r for r in elites if r.get("identity") == identity]
        if not rows:
            raise SystemExit(f"no elite for {identity}")
        ref = rows[0]["reference"]
        subprocess.run(
            ["nethackers", "pull", f"{ref['repo']}@{ref['commit']}", str(target)],
            check=True,
        )
    if not (target / "bot.py").is_file():
        raise SystemExit("seed has no bot.py")
    return target


def read_log(tree: Path) -> str:
    """The parent tree's `experience.md`, or an empty seed if it has none.

    A fresh seed from the hub carries no log, so iteration 1 starts with an
    empty string and the brief omits the section entirely. Once the agent has
    written one, every later iteration inherits it through the parent.
    """
    path = Path(tree) / "experience.md"
    if path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return ""


def _log_blocks(text: str) -> list[str]:
    """Split a log into its ``##``-headed entries."""
    return [
        b.strip()
        for b in re.split(r"\n(?=## )", text)
        if b.strip()
    ]


def _log_key(block: str) -> str:
    """A block's identity for dedup: its heading, or its whole text if it has
    none. Two entries from the same experiment share a heading, which is what
    makes "already tried" detectable without trusting the body."""
    for line in block.splitlines():
        if line.startswith("## "):
            return " ".join(line.lstrip("#").split()).lower()
    return " ".join(block.split()).lower()


def _is_placeholder_block(block: str) -> bool:
    """True for the unfilled form written into a fresh `experience.md`."""
    return bool(brief_mod._PLACEHOLDER_RE.search(block)) or block.lstrip(
        "# "
    ).strip().lower().startswith("experience.md")


def harvest_log(source: Path, target: Path) -> int:
    """Copy a discarded mutant's new log entries into the surviving parent.

    The log and the mutant are separate decisions, and the loop was conflating
    them. A `NOT-A-WIN` reverts the whole worktree, which throws away the
    agent's strategy code -- correctly, since the change did not help. But it
    also threw away `experience.md`, which is where the agent recorded *why*,
    and that is the one part worth keeping: run 36637347806 made and measured a
    change (0.0624 -> 0.0671, 3 seeds up / 2 down / 10 flat), correctly reverted
    it, and wrote 7336 bytes of log including the two findings that redirect the
    whole problem -- the score is the XP ladder and not depth, and 73-97% of XP
    comes from "normal" monsters. All of it was binned with the diff, so the next
    iteration would have re-derived it from scratch and possibly re-tried the
    same retreat change.

    Appending rather than overwriting matters for the same reason: the surviving
    parent may already hold earlier entries, and an experiment that failed is
    only worth not repeating if the entry that says so outlives it.

    Returns the number of characters added.
    """
    written = Path(source) / "experience.md"
    if not written.is_file():
        return 0
    new = written.read_text(encoding="utf-8", errors="replace").strip()
    if not new:
        return 0
    existing = read_log(target).strip()

    if not existing:
        # No log in the parent yet, so the whole file is new -- but the seeded
        # placeholder is not. Carrying the form forward would make the next
        # brief open on a template instead of on a finding.
        blocks = _log_blocks(new)
        kept = [b for b in blocks if not _is_placeholder_block(b)]
        if not kept:
            return 0
        (Path(target) / "experience.md").write_text("\n\n".join(kept) + "\n", encoding="utf-8")
        return len("\n\n".join(kept))

    # A block is the unit. Appending the whole file would re-add every entry the
    # parent already has, because the mutant was seeded from that parent and its
    # log necessarily starts with all of it; comparing whole files with `in` did
    # not catch that, since the longer string is not a substring of the shorter.
    # An experiment is only worth not repeating if its own entry survives, so
    # match on the heading and take only what the parent has not seen.
    seen = _log_blocks(existing)
    seen_keys = {_log_key(b) for b in seen}
    added: list[str] = []
    for block in _log_blocks(new):
        if _is_placeholder_block(block):
            continue
        key = _log_key(block)
        if key in seen_keys or any(key in k or k in key for k in seen_keys if k):
            continue
        seen_keys.add(key)
        added.append(block)
    if not added:
        return 0
    body = "\n".join(part for part in (existing, "\n\n".join(added)) if part)
    (Path(target) / "experience.md").write_text(body + "\n", encoding="utf-8")
    return len("\n\n".join(added))


#: Files the loop itself drops into the worktree. They are not the mutator's
#: edit, so a diff that reported them would bury the one that matters -- the
#: agent rewrites its experience log every turn, which is the expected case
#: rather than a change worth recording.
HARNESS_FILES = ("experience.md", "history.json", ".origin")

#: A patch is a record, not a copy. Enough to reconstruct what was tried and
#: why it scored the way it did; not enough to rebuild the tree from the log.
DIFF_CHARS = 8000


def _is_harness_artifact(rel: str) -> bool:
    name = rel.rsplit("/", 1)[-1]
    return (
        name in HARNESS_FILES
        or name.startswith("brief-")
        or name.startswith("transcript-")
        or name.endswith(".pyc")
        or "__pycache__" in rel
    )


def _read_text(path: Path) -> str | None:
    """File contents, or None if it is not text we should diff."""
    try:
        if path.stat().st_size > 2_000_000:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data[:8192]:
        return None
    return data.decode("utf-8", errors="replace")


def tree_diff(parent: Path, worktree: Path) -> dict:
    """What the mutator actually changed, as a stat and a patch.

    A run records the agent's *account* of its change -- `hypothesis` and
    `report`, a few thousand characters of its own prose -- and the *verdict*.
    It never recorded the edit itself. For a kept tree that is fine, the tree is
    the next parent. For a discarded one the code is binned, so after the
    transcript's 30 days the change exists only as a paragraph describing it,
    written by the party that has an interest in it reading as thorough. That is
    the weakest possible record of a failed experiment: an unverifiable claim
    about code nobody can see.

    The trees are plain directories (47 files, no `.git`), so this is a
    `difflib` walk rather than `git diff`, and it compares the worktree against
    the parent it was seeded from -- which is what "what did the mutator do this
    iteration" means.

    Returns `{"changed": [...], "patch": str, "truncated": bool}`. `changed` is
    always complete even when the patch is cut, because a stat that can itself
    be truncated is no use for deciding what to look at.
    """
    parent, worktree = Path(parent), Path(worktree)
    old: dict[str, str] = {}
    new: dict[str, str] = {}
    for base, store in ((parent, old), (worktree, new)):
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(base).as_posix()
            if _is_harness_artifact(rel):
                continue
            text = _read_text(path)
            if text is not None:
                store[rel] = text

    changed: list[dict] = []
    chunks: list[str] = []
    for rel in sorted(set(old) | set(new)):
        before, after = old.get(rel), new.get(rel)
        if before == after:
            continue
        if before is None:
            kind = "added"
        elif after is None:
            kind = "removed"
        else:
            kind = "modified"
        body = list(
            difflib.unified_diff(
                (before or "").splitlines(keepends=True),
                (after or "").splitlines(keepends=True),
                fromfile=f"a/{rel}" if before is not None else "/dev/null",
                tofile=f"b/{rel}" if after is not None else "/dev/null",
                n=3,
            )
        )
        added = sum(1 for line in body if line.startswith("+") and not line.startswith("+++"))
        removed = sum(1 for line in body if line.startswith("-") and not line.startswith("---"))
        changed.append({"file": rel, "change": kind, "+": added, "-": removed})
        chunks.append(f"diff --git a/{rel} b/{rel} ({kind})\n")
        chunks.extend(body)

    patch = "".join(chunks)
    truncated = len(patch) > DIFF_CHARS
    if truncated:
        patch = patch[:DIFF_CHARS] + f"\n... patch truncated at {DIFF_CHARS} chars\n"
    return {"changed": changed, "patch": patch, "truncated": truncated}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("identity")
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--operator", default="opencode2")
    parser.add_argument("--model", default="opencode/big-pickle")
    parser.add_argument("--seed-mode", default="hub", choices=["hub", "pinned", "autoascend"])
    parser.add_argument("--parent-ref")
    parser.add_argument("--workdir", default="runs")
    args = parser.parse_args()

    # ABSOLUTE, always. The mutator bind-mounts the worktree into the container
    # with `-v {worktree}:/workspace`, and Docker rejects a relative mount
    # source as an invalid volume name -- `docker run` exits 125 with
    # "includes invalid characters for a local volume name". A relative
    # --workdir therefore fails at the operator call, after the baseline has
    # already been scored, which is where an entire iteration goes to die.
    work = Path(args.workdir).resolve()
    work.mkdir(parents=True, exist_ok=True)

    print(f"=== {args.identity} · our loop · {args.iterations} iteration(s) ===", flush=True)
    parent = fetch_seed(args.identity, args.seed_mode, args.parent_ref)
    print(f"seed: {parent}", flush=True)

    parent_mean, parent_rows, _ = score(parent, args.identity)
    print(f"seed baseline: {parent_mean:.4f} over {len(parent_rows)} seeds", flush=True)
    diagnosis = {
        "identity": args.identity, "mean_progress": parent_mean, "results": parent_rows,
    }
    (work / "baseline.json").write_text(json.dumps(diagnosis, indent=2))

    best_tree = parent
    best_mean = parent_mean
    best_rows = parent_rows
    history = []

    for iteration in range(1, args.iterations + 1):
        print(f"\n--- iteration {iteration} ---", flush=True)

        worktree = work / f"work-{iteration}"
        if worktree.exists():
            shutil.rmtree(worktree)
        shutil.copytree(best_tree, worktree)

        # The log is read from the PARENT's tree, not the repository. The agent
        # writes its own entries into /workspace/experience.md, and copytree
        # carries them forward automatically -- a kept winner brings its written
        # experience to the next iteration, and so does a discarded mutant (with
        # it, into the bin). Reading from REPO_ROOT instead would splice in a
        # log belonging to a different parent, which is the one thing the
        # copytree already gets right for free.
        log_text = read_log(best_tree)
        print(f"experience log: {len(log_text)} chars from {best_tree.name}", flush=True)

        # Seed the log file if the parent has none, so the first turn reads a
        # file rather than a missing path. The agent's first action on run
        # 36637347806 was `read /workspace/experience.md`, which returned
        # "File not found", and its reaction was "No experience.md yet. This is
        # the first turn. Let me read the bot code." -- correct, and it went on
        # to work. But it had to infer the protocol from a failed read, and a
        # model that reads a missing file as "this project does not use one"
        # would never write it. A seeded file with the entry template in it
        # makes the contract a property of the workspace rather than a
        # convention the agent has to infer.
        if not (worktree / "experience.md").is_file():
            (worktree / "experience.md").write_text(
                f"# experience.md — {args.identity}\n\n"
                "This log is written by the agent, one entry per iteration. It is\n"
                "the loop's only memory: the next turn reads it before choosing\n"
                "what to try, so an attempt recorded as failed is not repeated.\n\n"
                "Append an entry below, using this structure:\n\n"
                "## <YYYY-MM-DD> — <identity> — <short title>\n\n"
                "**Problem:**\n<the situation that led to death or a low score>\n\n"
                "**Hypotheses:**\n- <possible cause #1>\n\n"
                "**Attempts:**\n- <what you tried, and the measured result>\n\n"
                "**What worked:**\n<the change that helped, with evidence, or "
                '"nothing yet">\n',
                encoding="utf-8",
            )
            print("seeded an empty experience.md in the worktree", flush=True)

        brief_text = brief_mod.build(args.identity, diagnosis, log_text)
        (work / f"brief-{iteration}.md").write_text(brief_text)
        print(f"brief: {len(brief_text)} chars -> {work}/brief-{iteration}.md", flush=True)

        hypothesis, report = run_operator(
            worktree, brief_text, args, transcript=work / f"transcript-{iteration}.log"
        )
        source = "tree-comment"
        if not hypothesis:
            hypothesis = condense_report(report)
            source = "closing-message" if hypothesis else "none"
        print(f"operator done; hypothesis [{source}]: {hypothesis!r}", flush=True)

        # What it actually changed, recorded before the verdict. Order matters
        # only in that the diff is of the tree as the agent left it, so it has
        # to be taken before anything rewrites the worktree -- and nothing here
        # does, but the harvest below does.
        edit = tree_diff(best_tree, worktree)
        if edit["changed"]:
            summary = ", ".join(
                f"{c['file']} ({c['change']} +{c['+']}/-{c['-']})"
                for c in edit["changed"][:4]
            )
            more = f" +{len(edit['changed']) - 4} more" if len(edit["changed"]) > 4 else ""
            print(f"edit: {len(edit['changed'])} file(s): {summary}{more}", flush=True)
        else:
            print("edit: none — the tree came back unchanged", flush=True)
        (work / f"diff-{iteration:03d}.patch").write_text(edit["patch"], encoding="utf-8")

        smoke_mean, _, _ = score(
            worktree, args.identity, seeds=1, max_steps=SMOKE_STEPS
        )
        print(f"smoke: {smoke_mean:.4f}", flush=True)

        child_mean, child_rows, child_raw = score(worktree, args.identity)
        verdict = mean_gate(child_mean, best_mean, paired_verdict(child_rows, best_rows))
        print(
            f"child {child_mean:.4f} vs parent {best_mean:.4f} -> {verdict['verdict']}: "
            f"{verdict['why']}",
            flush=True,
        )

        history.append({
            "iteration": iteration, "child_mean": child_mean,
            "parent_mean": best_mean, "hypothesis": hypothesis,
            "hypothesis_source": source,
            "report": (report or "")[:REPORT_CHARS] or None,
            # The stat, not the patch. history.json is the file that gets
            # summarised and read by eye, and the patch already lives in
            # diff-<n>.patch next to it -- duplicating up to DIFF_CHARS per
            # iteration here would double the record for no gain.
            "edit": {"changed": edit["changed"], "truncated": edit["truncated"]},
            **verdict,
        })
        (work / "history.json").write_text(json.dumps(history, indent=2))

        if verdict["verdict"] in KEEPING_VERDICTS:
            kept = work / f"winner-{iteration}"
            if kept.exists():
                shutil.rmtree(kept)
            shutil.copytree(worktree, kept)
            best_tree, best_mean, best_rows = kept, child_mean, child_rows
            print(
                f"KEPT as the new parent: {kept}"
                + ("" if verdict["verdict"] == "WIN" else
                   f"  (a {verdict['verdict']}, not a publishable win)"),
                flush=True,
            )
        else:
            # The mutant's code is binned, but its log is not. An agent that
            # measured a change, found it did not work, and wrote down why has
            # produced the most valuable output of the iteration, and that
            # output does not depend on the change having worked. Without this,
            # a failed experiment is invisible to the next iteration and
            # nothing is learned from it -- see harvest_log.
            carried = harvest_log(worktree, best_tree)
            if carried:
                print(
                    f"reverted the mutant but carried {carried} chars of its "
                    f"experience.md into the next parent",
                    flush=True,
                )

            # A WIN leaves the machine on its own: the loop is meant to improve
            # itself without anyone watching, so a cleared result is pushed and
            # registered here rather than logged for a human to notice later.
            # KEEP deliberately does not publish -- it is a better place to
            # search from, not a better bot.
            if verdict["verdict"] == "WIN":
                record = publish_mod.register_winner(
                    kept, args.identity, child_mean, child_raw, ARENA_IMAGE, work,
                    run_id=os.environ.get("GITHUB_RUN_ID", "local"),
                )
                history[-1]["publish"] = record
                (work / "history.json").write_text(json.dumps(history, indent=2))
                if record.get("published"):
                    print(
                        f"published: branch {record['branch']} commit "
                        f"{record['commit'][:12]} registered to {record['repo']}",
                        flush=True,
                    )
                else:
                    print(
                        f"NOT published ({record.get('error', 'unknown')}); "
                        f"the tree is still kept at {kept}",
                        flush=True,
                    )

    # Whatever happened, the run's output is worth keeping. A run that ends in
    # NOT-A-WIN has still measured seeds and written down why, and run
    # 36710578461 lost 4186 characters of exactly that to a workspace that died
    # with the job. `harvest_log` covers iteration to iteration; this covers the
    # end of the run. Not registered to the hub -- a lost program is not a
    # submission -- and not read by the next run, which stays independent.
    published = publish_mod.publish_results(
        best_tree, args.identity, work, run_id=os.environ.get("GITHUB_RUN_ID", "local")
    )
    if published.get("published"):
        print(
            f"results published: branch {published['branch']} "
            f"commit {published['commit'][:12]}",
            flush=True,
        )
    else:
        print(
            f"results NOT published ({published.get('error', 'unknown')}); "
            f"they are in the artifact",
            flush=True,
        )
    (work / "history.json").write_text(json.dumps(history, indent=2))

    print(f"\n=== done · {len(history)} iteration(s) ===")
    for entry in history:
        print(f"  {entry['iteration']}: {entry['verdict']:11} {entry['why']}")
    return 0


def run_operator(
    worktree: Path, brief_text: str, args, transcript: Path | None = None
) -> tuple[str | None, str | None]:
    """Drive the project's mutator, passing OUR brief.

    Reuses `ContainerOperator`, so the sandbox caps, the platform args and the
    agent CLI are the project's, not ours. The only thing we change is the
    string handed to the agent.

    Streams the agent's own output to `transcript` while it runs.
    `run_operator` passes **every line of the agent's stdout** to `on_line`, and
    E8 showed why that matters: it spent 10.0 M tokens and left the tree
    byte-identical to its parent, with `hypothesis: None` and no other evidence
    of what it did. A no-op is indistinguishable from a crash, a refusal, and
    "it read everything and decided nothing was worth doing" -- and those need
    three different fixes. The transcript is the only thing that tells them
    apart.

    Returns `(hypothesis_in_the_tree, closing_message)`. The caller decides what
    to do when the first is None and the second is not.
    """
    from nethackers.harness.container_operator import ContainerOperator

    operator = ContainerOperator(
        harness=args.operator, image=MUTATOR_IMAGE, model=args.model,
    )

    handle = None
    written = 0
    said = ""
    if transcript is not None:
        transcript.parent.mkdir(parents=True, exist_ok=True)
        handle = transcript.open("w", encoding="utf-8")

    def on_line(line: str) -> None:
        # Best-effort and non-fatal: losing transcript lines must never take
        # down the run they were meant to explain.
        nonlocal written, said
        utterance = _speech_in(line)
        if utterance:
            said = utterance
        if handle is None:
            return
        try:
            handle.write(line if line.endswith("\n") else line + "\n")
            written += len(line)
            # Flush often. A run that dies mid-iteration is exactly the case
            # where the partial transcript is the only evidence, and buffered
            # lines are lost with the process.
            if written > 64_000:
                handle.flush()
                written = 0
        except Exception:
            pass

    # Wall-clock ceiling on the turn, via the operator's own `stop` hook: the
    # watcher thread sees the event set and kills the container, so this is a
    # real stop rather than a detached `communicate(timeout=...)` -- the
    # harness/loop.py pattern. `cancelled` says whether *we* stopped it, because
    # `OperatorResult.stopped_reason` cannot distinguish our budget from the
    # agent's own decision to finish.
    stop = threading.Event()
    cancelled = threading.Event()
    timer = threading.Timer(
        AGENT_TIMEOUT_SECONDS,
        lambda: (cancelled.set(), stop.set()),
    )
    timer.daemon = True
    timer.start()
    try:
        result = operator.run(worktree, brief_text, on_line=on_line, stop=stop)
    finally:
        # Always cancel, or a completed turn leaves a live timer holding the
        # event (and, under a short AGENT_TIMEOUT_SECONDS, a later iteration's
        # timer firing into the next one).
        timer.cancel()
        if handle is not None:
            try:
                handle.flush()
                handle.close()
            except Exception:
                pass
    if cancelled.is_set():
        print(
            f"  agent hit the {AGENT_TIMEOUT_SECONDS // 60}-minute ceiling; "
            f"container stopped. Whatever it wrote is still scored, and its "
            f"transcript is still the evidence of what it was doing.",
            flush=True,
        )

    usage = getattr(result, "usage", None)
    total = None
    if usage is not None:
        total = sum(
            int(getattr(usage, field, 0) or 0)
            for field in ("input", "output", "cache_creation", "cache_read")
        )
    if transcript is not None:
        size = transcript.stat().st_size if transcript.is_file() else 0
        print(
            f"  transcript: {transcript} ({size} bytes) -- read this before "
            f"guessing why the mutation was what it was",
            flush=True,
        )
    print(
        f"  backend={getattr(result, 'backend', '?')} tokens={total} "
        f"stop={getattr(result, 'stopped_reason', '?')}",
        flush=True,
    )
    return extract_hypothesis(worktree), said


def _speech_in(line: str) -> str | None:
    """The assistant's prose in one transcript line, if it carries any.

    A hypothesis is a thing the agent SAYS as much as a thing it writes in the
    tree, and the tree is the wrong place to look for the one case that matters
    most. An agent that tries a change, measures it, and reverts leaves the tree
    exactly as it found it -- comment included -- so `extract_hypothesis` reads
    nothing and the run records `hypothesis: None`. That is precisely the run
    with the most to say: 17.7 M tokens, a 90-seed paired test, and a
    deliberately discarded result.

    The agent CLI streams JSONL, one object per line, and its prose arrives as
    `{"type": "text", "part": {"type": "text", "text": ...}}`. Take the last
    one: the closing message is the report.
    """
    line = line.strip()
    if not line or not line.startswith("{"):
        return None
    try:
        event = json.loads(line)
    except ValueError:
        return None
    part = event.get("part")
    if not isinstance(part, dict) or part.get("type") != "text":
        return None
    text = part.get("text")
    return text if isinstance(text, str) and text.strip() else None


# A hypothesis is a COMMENT BLOCK, not a line. The regex used to be
# `# hypothesis: (.+)` with no DOTALL, so it stopped at the first newline and
# returned half a sentence whenever the model wrote its rationale across
# several lines -- which it does, reliably, when the brief asks for one.
#
# The text runs from the marker to the next line that starts a new comment or a
# new top-level definition, which is where the author's reasoning about *this*
# change ends. Contiguity is what marks it out: a block broken by unrelated code
# is two separate comments, not one hypothesis.
_HYP_START = __import__("re").compile(r"^\s*#\s*hypothesis:\s*(.*)$", __import__("re").IGNORECASE)
# A continuation line is any indented comment. The earlier pattern used a
# negative lookahead for `hypothesis:`, which matched the SECOND and later
# lines of the same block and truncated the hypothesis to one line -- which
# is exactly the bug this replaces. So: a comment line at the SAME
# indentation as the marker continues it; a differently-indented comment, or
# any code, ends it.
_HYP_STOP = __import__("re").compile(r"^\s*(?:def |class |@)")


def _hypothesis_blocks(text: str) -> list[str]:
    """Every `# hypothesis:` comment block in one file, in order."""
    lines = text.splitlines()
    out: list[str] = []
    index = 0
    while index < len(lines):
        start = _HYP_START.match(lines[index])
        if not start:
            index += 1
            continue
        block = [start.group(1).strip()]
        index += 1
        while index < len(lines):
            if _HYP_STOP.match(lines[index]):
                break
            stripped = lines[index].strip()
            if stripped.startswith("#"):
                block.append(stripped.lstrip("#").strip())
            elif stripped:
                break  # code, not prose: the hypothesis ended
            else:
                break
            index += 1
        joined = " ".join(part for part in block if part).strip()
        if joined:
            out.append(joined)
    return out


def extract_hypothesis(tree: Path) -> str | None:
    """Read the mutation's own `# hypothesis:` comment.

    The worktree is a copy of the parent, so it inherits every ancestor's
    comment. Only a line absent from the parent counts as this mutation's --
    the same rule the project's `_hypothesis_of` applies.
    """
    found: list[str] = []
    for path in sorted(tree.rglob("*.py")):
        try:
            found.extend(_hypothesis_blocks(path.read_text()))
        except (OSError, UnicodeDecodeError):
            continue
    return found[0] if found else None


#: Markdown headings, so a closing report can be taken apart into sections.
_HEADING = __import__("re").compile(r"^\s{0,3}#{1,6}\s*(.+?)\s*#*\s*$")
#: Section names that answer "what did you change and why", which is the whole
#: question a hypothesis exists to answer.
_ABOUT_THE_CHANGE = __import__("re").compile(
    r"hypoth|what i (tried|changed|did|attempted)|the change|summary|tl;?dr|approach",
    __import__("re").IGNORECASE,
)
#: A hypothesis is a line a human skims, not the report it came from.
HYPOTHESIS_CHARS = 400
#: The closing message is kept whole-ish, because that is what a human reads.
REPORT_CHARS = 4000


def _prose_lines(block: str) -> list[str]:
    """The sentences in one markdown section, minus furniture."""
    out: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("|", ">", "-", "*", "#")):
            continue
        if re.match(r"^`{3,}", stripped):
            continue
        out.append(stripped)
    return out


def _sections(text: str) -> list[tuple[str | None, str]]:
    body: list[str] = []
    heading: str | None = None
    blocks: list[tuple[str | None, str]] = []
    for line in text.splitlines():
        match = _HEADING.match(line)
        if match:
            if body:
                blocks.append((heading, "\n".join(body)))
            heading, body = match.group(1), []
        else:
            body.append(line)
    if body:
        blocks.append((heading, "\n".join(body)))
    return blocks


def condense_report(text: str | None, limit: int = HYPOTHESIS_CHARS) -> str | None:
    """One skimmable line out of the agent's closing message.

    Prefers the section that names the change, because an agent that reverts
    usually opens with the verdict ("I reverted the change") and puts the actual
    mechanism one heading later. Falls back to the first section with prose in
    it, so a report with unfamiliar headings still yields something.
    """
    if not text or not text.strip():
        return None
    sections = _sections(text)
    chosen = None
    for heading, block in sections:
        if heading and _ABOUT_THE_CHANGE.search(heading) and _prose_lines(block):
            chosen = block
            break
    if chosen is None:
        for _heading, block in sections:
            if _prose_lines(block):
                chosen = block
                break
    if chosen is None:
        return None
    joined = " ".join(_prose_lines(chosen))
    joined = re.sub(r"\s+", " ", joined).strip()
    if not joined:
        return None
    if len(joined) <= limit:
        return joined
    cut = joined[:limit].rsplit(" ", 1)[0]
    return f"{cut.rstrip(',.;:')}..."


if __name__ == "__main__":
    sys.exit(main())
