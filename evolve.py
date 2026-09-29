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
import json
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

def _find_repo_root(start: Path) -> Path:
    """The directory holding experience.md / experiments.md.

    See the same function in brief.py for why this searches upward and stops
    before the filesystem root. Running from the repository root rather than
    from loop/ was the difference between an 8,000-character brief and a
    3,600-character one that silently contained none of the notes.
    """
    for candidate in [start, *start.parents]:
        if candidate.parent == candidate:
            break
        if (candidate / "experience.md").is_file() or (candidate / "experiments.md").is_file():
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

#: One cheap episode on a reserved seed, to reject a mutant that does not run.
SMOKE_SEED = 9000
SMOKE_STEPS = 2000

#: A win needs most seeds forward, and a floor in absolute terms. A 4-up-3-down
#: split is a coin flip under a sign test, so it is not a win.
MIN_SEEDS_FORWARD = 5
MIN_TWO_THIRDS = True

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
    """
    from nethackers.harness import evaluate as E

    mean, evidence = E.evaluate(
        str(tree), spec_for(identity, seeds, max_steps), ARENA_IMAGE,
        now=now(), runtime="docker", max_parallel_evals=1,
    )
    results = [
        {
            "seed": r.trajectory_id, "turns": r.turns, "depth": r.max_depth,
            "progress": r.progress, "death": r.cause_of_death, "status": r.status,
        }
        for r in evidence.results
    ]
    return mean, results, [r.__dict__ for r in evidence.results]


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

        brief_text = brief_mod.build(
            args.identity,
            diagnosis,
            (REPO_ROOT / "experience.md").read_text(encoding="utf-8", errors="replace")
            if (REPO_ROOT / "experience.md").is_file() else "",
            (REPO_ROOT / "experiments.md").read_text(encoding="utf-8", errors="replace")
            if (REPO_ROOT / "experiments.md").is_file() else "",
        )
        (work / f"brief-{iteration}.md").write_text(brief_text)
        print(f"brief: {len(brief_text)} chars -> {work}/brief-{iteration}.md", flush=True)

        worktree = work / f"work-{iteration}"
        if worktree.exists():
            shutil.rmtree(worktree)
        shutil.copytree(best_tree, worktree)

        hypothesis, report = run_operator(
            worktree, brief_text, args, transcript=work / f"transcript-{iteration}.log"
        )
        source = "tree-comment"
        if not hypothesis:
            hypothesis = condense_report(report)
            source = "closing-message" if hypothesis else "none"
        print(f"operator done; hypothesis [{source}]: {hypothesis!r}", flush=True)

        smoke_mean, _, _ = score(
            worktree, args.identity, seeds=1, max_steps=SMOKE_STEPS
        )
        print(f"smoke: {smoke_mean:.4f}", flush=True)

        child_mean, child_rows, child_raw = score(worktree, args.identity)
        verdict = paired_verdict(child_rows, best_rows)
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

    try:
        result = operator.run(worktree, brief_text, on_line=on_line)
    finally:
        if handle is not None:
            try:
                handle.flush()
                handle.close()
            except Exception:
                pass

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
