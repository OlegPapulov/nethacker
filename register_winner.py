"""Publish a winning tree to the leaderboard, unattended.

The loop is supposed to improve itself without anyone watching, so a WIN has
to leave the machine on its own. That is two acts, not one, and conflating
them is the mistake this module exists to avoid:

  1. push the tree to `github.com/<owner>/nethacker`  -- transport
  2. `nethackers register --repo --commit --evidence` -- the actual submission

`git push` alone publishes nothing. The hub only learns a commit exists when
`register` POSTs `{reference, manifest, evidence}` to it, and it answers a
pushed-but-unregistered tree with exactly the same silence as no tree at all.
So a loop that pushes and stops looks identical, from the board, to a loop that
did nothing -- which is how "registration enabled" once coexisted with a
structurally incapable workflow (`evolve.yml`, the `--offline` note).

Publishing is deliberately best-effort and never raises. The run's real output
is the tree; a run that dies in here because a token expired would throw away
an iteration's agent call and 15 episodes to produce no tree at all. Every
failure comes back as `{"published": False, ...}` for `history.json`, so a
broken credential shows up as an explicit record instead of a silent gap.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from register_evidence import build_payload, write_payload

#: Each result gets its own branch. The leaderboard pins an exact
#: repo@commit, so a per-run ref keeps every published result fetchable at a
#: stable address, and keeps a publish from racing the run's own commit to
#: `main` (which is a fast-forward target, and fast-forwards lose races).
BRANCH_PREFIX = "evolve"


def default_repo() -> str | None:
    """The repo to publish into, read from this checkout's own origin remote.

    Derived rather than hardcoded so a fork or a renamed repo does not silently
    register rows against the wrong account. `normalize_github_ref` is the
    project's own parser and is the same validation the hub applies.
    """
    from nethackers.github_ref import NonGitHubRef, normalize_github_ref

    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return normalize_github_ref(url)
    except (subprocess.CalledProcessError, NonGitHubRef):
        return None


def register_winner(
    tree: Path,
    identity: str,
    mean: float,
    results: list[dict],
    arena_image: str,
    work: Path,
    *,
    run_id: str = "local",
    repo: str | None = None,
) -> dict:
    """Push `tree` and register it. Returns a record for `history.json`."""
    from nethackers.hubclient.publish import PublishError, publish_solution

    ref = f"{BRANCH_PREFIX}/{identity}-{run_id}"
    evidence_path = work / f"evidence-{identity}.json"
    record: dict = {"published": False, "branch": ref, "repo": repo}

    slug = repo or default_repo()
    if not slug:
        record["error"] = "no origin remote; cannot resolve a repo to publish into"
        return record
    record["repo"] = slug

    try:
        commit = publish_solution(
            tree, slug,
            message=f"{identity}: loop win (mean {mean:.4f})",
            ref=ref, workdir=work / f"publish-{identity}",
        )
    except PublishError as exc:
        record["error"] = f"push failed: {exc}"
        return record
    record["commit"] = commit

    write_payload(
        build_payload(Path(tree), identity, mean, results, arena_image), evidence_path
    )
    record["evidence"] = str(evidence_path)

    try:
        proc = subprocess.run(
            [
                "nethackers", "register",
                "--repo", slug, "--commit", commit, "--evidence", str(evidence_path),
                "-o", "json",
            ],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        record["error"] = "nethackers not on PATH"
        return record

    if proc.returncode != 0:
        record["error"] = (proc.stderr or proc.stdout or "register failed").strip()[:600]
        return record

    try:
        record["response"] = json.loads(proc.stdout)
    except json.JSONDecodeError:
        record["response"] = (proc.stdout or "").strip()[:600]

    record["published"] = True
    return record


RESULTS_BRANCH_PREFIX = "evolve-result"


def publish_results(
    parent: Path,
    identity: str,
    work: Path,
    *,
    run_id: str = "local",
    repo: str | None = None,
) -> dict:
    """Push a run's results -- kept trees and the agent's log -- to a branch.

    A run that ends in `NOT-A-WIN` has still produced the thing the loop
    exists to produce: seeds measured, causes identified, and an
    `experience.md` saying what was tried and what it was worth. Run
    36710578461 found two real defects (stale corpse entries never removed,
    the corpse hunt throttled to `.every(5)`) and then had all 4186 characters
    of that written into a workspace that died with the job. `harvest_log`
    carries a rejected mutant's log to the *next iteration*; nothing carried it
    out of the *run*.

    This is deliberately not `nethackers register`. Registration is a claim
    that a program is worth scoring against other people's, and a program that
    lost is not that: putting a 0.06 on the board beside real entries would
    misrepresent the state of the work. A results branch is a record, not a
    submission, and the hub never sees it.

    Nor is this read back by the next run. Runs stay independent by design --
    each seeds fresh and re-derives what it needs -- so this is a place to put
    the output where it cannot quietly become the next run's assumptions.

    Best-effort, like `register_winner`: never raises, returns a record.
    """
    ref = f"{RESULTS_BRANCH_PREFIX}/{identity}-{run_id}"
    record: dict = {"published": False, "branch": ref}
    slug = repo or default_repo()
    if not slug:
        record["error"] = "no origin remote; cannot resolve a repo to publish into"
        return record
    record["repo"] = slug

    log = parent / "experience.md"
    if not log.is_file():
        record["error"] = "parent has no experience.md; nothing to publish"
        return record

    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        record["error"] = f"no origin remote: {exc}"
        return record

    history = work / "history.json"
    try:
        commit = _push_results_branch(
            work / f"results-{identity}", url, ref, parent, log, history, identity
        )
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        record["error"] = f"push failed: {exc}"
        return record

    record["commit"] = commit
    record["published"] = True
    return record


def _push_results_branch(
    workdir: Path,
    url: str,
    ref: str,
    parent: Path,
    log: Path,
    history: Path | None,
    identity: str,
) -> str:
    """Stage the results and push them as an orphan branch.

    An orphan branch rather than a commit on `main` or on an existing ref: the
    results are a snapshot, they should not race the run's own commit to `main`
    (a fast-forward target, and fast-forwards lose races), and a branch that
    already exists from a re-run should be replaced rather than built on.
    """
    if workdir.exists():
        shutil.rmtree(workdir)
    stage = workdir / "stage"
    stage.mkdir(parents=True)

    (stage / "experience.md").write_text(
        log.read_text(encoding="utf-8", errors="replace"), encoding="utf-8"
    )
    if history.is_file():
        shutil.copy2(history, stage / "history.json")
    for kept in sorted(parent.parent.glob("winner-*")):
        if kept.is_dir():
            shutil.copytree(kept, stage / kept.name)

    def git(*args: str) -> str:
        proc = subprocess.run(
            ["git", *args], cwd=stage, capture_output=True, text=True, check=False
        )
        if proc.returncode != 0:
            # git writes the reason to stderr and nothing useful to stdout, and
            # a bare CalledProcessError hides which of the six calls failed.
            raise RuntimeError(
                f"git {args[0]} failed ({proc.returncode}): "
                f"{(proc.stderr or proc.stdout).strip()[:300]}"
            )
        return proc.stdout.strip()

    git("init", "-q")
    git("checkout", "-q", "--orphan", "results")
    git("add", "-A")
    git(
        "-c", "user.name=nethackers-our-evolve",
        "-c", "user.email=nethackers-our-evolve@users.noreply.github.com",
        "commit", "-q", "-m", f"{identity}: results for run {ref.rsplit('/', 1)[-1].rsplit('-', 1)[-1]}",
    )
    git("remote", "add", "origin", url)
    git("push", "--force", "-q", "origin", "HEAD:refs/heads/" + ref)
    return git("rev-parse", "HEAD")
