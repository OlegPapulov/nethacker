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
